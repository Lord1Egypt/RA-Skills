// @ts-nocheck
/**
 * guard-scanner v8 — CI/CD Reporter
 *
 * @security-manifest
 *   env-read: [GITHUB_OUTPUT, GITHUB_STEP_SUMMARY]
 *   env-write: []
 *   network: [webhook URL if configured]
 *   fs-read: []
 *   fs-write: [GitHub annotations file]
 *   exec: none
 *   purpose: CI/CD pipeline integration for guard-scanner results
 */

import fs  from 'fs';
import https  from 'https';

class CIReporter {
    constructor(options = {}) {
        this.format = options.format || 'github'; // github | gitlab | webhook
        this.verbose = options.verbose || false;
    }

    // ── GitHub Actions Annotations ────────────────────────────
    toGitHubAnnotations(findings) {
        const annotations = [];
        for (const skill of findings) {
            for (const f of (skill.findings || [])) {
                const level = f.severity === 'CRITICAL' ? 'error' :
                    f.severity === 'HIGH' ? 'error' :
                        f.severity === 'MEDIUM' ? 'warning' : 'notice';
                annotations.push({
                    level,
                    message: `[${f.id}] ${f.desc}`,
                    file: f.file || skill.skill || 'unknown',
                    line: f.line || 1,
                    col: 1,
                });
            }
        }
        return annotations;
    }

    // GitHub Actions workflow commands (stdout format)
    printGitHubAnnotations(findings) {
        const annotations = this.toGitHubAnnotations(findings);
        for (const a of annotations) {
            // ::error file={name},line={line},col={col}::{message}
            console.log(`::${a.level} file=${a.file},line=${a.line},col=${a.col}::${a.message}`);
        }
        return annotations.length;
    }

    // GitHub step summary (markdown)
    toGitHubSummary(findings, stats) {
        let md = '## 🛡️ Guard Scanner Report\n\n';
        md += `| Metric | Value |\n|---|---|\n`;
        md += `| Scanned | ${stats.scanned || 0} |\n`;
        md += `| Clean | ${stats.clean || 0} |\n`;
        md += `| Suspicious | ${stats.suspicious || 0} |\n`;
        md += `| Malicious | ${stats.malicious || 0} |\n\n`;

        if (findings.length > 0) {
            md += '### Findings\n\n';
            md += '| Skill | Verdict | Risk | Findings |\n|---|---|---|---|\n';
            for (const s of findings) {
                md += `| ${s.skill} | ${s.verdict} | ${s.risk} | ${s.findings?.length || 0} |\n`;
            }
        }
        return md;
    }

    // Write summary to $GITHUB_STEP_SUMMARY
    writeGitHubSummary(findings, stats) {
        const summaryPath = process.env.GITHUB_STEP_SUMMARY;
        if (summaryPath) {
            const md = this.toGitHubSummary(findings, stats);
            fs.appendFileSync(summaryPath, md);
            return true;
        }
        return false;
    }

    // ── GitLab Code Quality ────────────────────────────────────
    toGitLabCodeQuality(findings) {
        const issues = [];
        for (const skill of findings) {
            for (const f of (skill.findings || [])) {
                issues.push({
                    type: 'issue',
                    check_name: f.id,
                    description: f.desc,
                    categories: [f.cat],
                    severity: f.severity === 'CRITICAL' ? 'blocker' :
                        f.severity === 'HIGH' ? 'critical' :
                            f.severity === 'MEDIUM' ? 'major' : 'minor',
                    location: {
                        path: f.file || skill.skill || 'unknown',
                        lines: { begin: f.line || 1 },
                    },
                    fingerprint: `${f.id}-${f.file || skill.skill}-${f.line || 0}`,
                });
            }
        }
        return issues;
    }

    // ── Webhook Notification ───────────────────────────────────
    async sendWebhook(url, payload) {
        if (!url) throw new Error('Webhook URL is required');
        return new Promise((resolve, reject) => {
            const data = JSON.stringify(payload);
            const urlObj = new URL(url);
            const req = https.request({
                hostname: urlObj.hostname,
                port: urlObj.port || 443,
                path: urlObj.pathname + urlObj.search,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(data),
                },
            }, (res) => {
                let body = '';
                res.on('data', chunk => { body += chunk; });
                res.on('end', () => resolve({ status: res.statusCode, body }));
            });
            req.on('error', reject);
            req.setTimeout(15000, () => { req.destroy(); reject(new Error('Webhook timeout')); });
            req.write(data);
            req.end();
        });
    }
}

export {  CIReporter  };
