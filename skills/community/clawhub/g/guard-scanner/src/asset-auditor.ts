// @ts-nocheck
/**
 * guard-scanner v6.0.0 — Asset Auditor
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: [npm registry API, GitHub REST API]
 *   fs-read: []
 *   fs-write: []
 *   exec: [clawhub CLI (optional)]
 *   purpose: Audit npm/GitHub/ClawHub assets for accidental exposure
 */

import https  from 'https';
import { execSync  } from 'child_process';

const AUDIT_VERSION = '8.0.0';

// ── HTTP helper (no external deps) ─────────────────────────────────
function httpGet(url, options = {}) {
    return new Promise((resolve, reject) => {
        const timeout = options.timeout || 15000;
        const urlObj = new URL(url);
        const reqOptions = {
            hostname: urlObj.hostname,
            port: urlObj.port || 443,
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            headers: {
                'User-Agent': `guard-scanner/${AUDIT_VERSION}`,
                'Accept': 'application/json',
                ...(options.headers || {}),
            },
        };

        const req = https.request(reqOptions, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    try {
                        resolve({ status: res.statusCode, data: JSON.parse(data) });
                    } catch (e) {
                        resolve({ status: res.statusCode, data: data });
                    }
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0, 200)}`));
                }
            });
        });

        req.on('error', reject);
        req.setTimeout(timeout, () => {
            req.destroy();
            reject(new Error(`Timeout after ${timeout}ms: ${url}`));
        });
        req.end();
    });
}

// ── Alert severity levels ──────────────────────────────────────────
const ALERT_SEVERITY = {
    CRITICAL: 'CRITICAL',
    HIGH: 'HIGH',
    MEDIUM: 'MEDIUM',
    LOW: 'LOW',
    INFO: 'INFO',
};

// ── AssetAuditor class ─────────────────────────────────────────────
class AssetAuditor {
    constructor(options = {}) {
        this.verbose = options.verbose || false;
        this.format = options.format || 'text';
        this.quiet = options.quiet || false;
        this.timeout = options.timeout || 15000;
        this.results = { npm: null, github: null, clawhub: null };
        this.alerts = [];
        this._httpGet = options._httpGet || httpGet; // DI for testing
    }

    // ── npm Audit ──────────────────────────────────────────────────
    async auditNpm(username) {
        if (!username) throw new Error('npm username is required');
        const results = { packages: [], alerts: [] };

        try {
            // Search by author
            const authorRes = await this._httpGet(
                `https://registry.npmjs.org/-/v1/search?text=author:${encodeURIComponent(username)}&size=250`,
                { timeout: this.timeout }
            );

            // Search by maintainer (may catch different packages)
            const maintainerRes = await this._httpGet(
                `https://registry.npmjs.org/-/v1/search?text=maintainer:${encodeURIComponent(username)}&size=250`,
                { timeout: this.timeout }
            );

            // Merge and deduplicate
            const seen = new Set();
            const allPackages = [];
            for (const res of [authorRes, maintainerRes]) {
                if (res.data && res.data.objects) {
                    for (const obj of res.data.objects) {
                        const pkg = obj.package;
                        if (!seen.has(pkg.name)) {
                            seen.add(pkg.name);
                            allPackages.push({
                                name: pkg.name,
                                version: pkg.version,
                                description: pkg.description || '',
                                scope: pkg.scope || 'unscoped',
                                date: pkg.date,
                                links: pkg.links || {},
                            });
                        }
                    }
                }
            }

            results.packages = allPackages;

            // ── Detect anomalies ───────────────────────────────────
            // 1. Multiple scopes for same base name
            const baseNames = new Map();
            for (const pkg of allPackages) {
                const baseName = pkg.name.replace(/^@[^/]+\//, '');
                if (!baseNames.has(baseName)) {
                    baseNames.set(baseName, []);
                }
                baseNames.get(baseName).push(pkg.name);
            }
            for (const [base, names] of baseNames) {
                if (names.length > 1) {
                    results.alerts.push({
                        severity: ALERT_SEVERITY.HIGH,
                        type: 'SCOPE_DUPLICATE',
                        message: `Package "${base}" published under multiple scopes: ${names.join(', ')}`,
                        affected: names,
                    });
                }
            }

            // 2. Check each package for suspicious patterns
            for (const pkg of allPackages) {
                // Get detailed package info
                try {
                    const detailRes = await this._httpGet(
                        `https://registry.npmjs.org/${pkg.name}`,
                        { timeout: this.timeout }
                    );
                    const detail = detailRes.data;
                    const latestVersion = detail['dist-tags']?.latest;
                    const latestData = latestVersion ? detail.versions?.[latestVersion] : null;

                    if (latestData) {
                        // Check if src/ or node_modules/ included
                        const files = latestData.files || [];
                        const hasNodeModules = files.some(f => f === 'node_modules/' || f.startsWith('node_modules'));
                        const hasSrc = files.some(f => f === 'src/' || f.startsWith('src'));
                        const hasEnv = files.some(f => f === '.env' || f.includes('.env'));

                        if (hasNodeModules) {
                            results.alerts.push({
                                severity: ALERT_SEVERITY.CRITICAL,
                                type: 'NODE_MODULES_IN_PACKAGE',
                                message: `Package "${pkg.name}" includes node_modules/ in published files`,
                                affected: [pkg.name],
                            });
                        }

                        if (hasEnv) {
                            results.alerts.push({
                                severity: ALERT_SEVERITY.CRITICAL,
                                type: 'ENV_FILE_IN_PACKAGE',
                                message: `Package "${pkg.name}" includes .env file in published files`,
                                affected: [pkg.name],
                            });
                        }

                        // Check publishConfig
                        const isPublic = latestData.publishConfig?.access === 'public' ||
                            (!latestData.publishConfig?.access && !pkg.name.startsWith('@'));
                        if (isPublic && !latestData.private) {
                            results.alerts.push({
                                severity: ALERT_SEVERITY.INFO,
                                type: 'PUBLIC_PACKAGE',
                                message: `Package "${pkg.name}" is publicly accessible`,
                                affected: [pkg.name],
                            });
                        }
                    }
                } catch (e) {
                    // Package detail fetch failed — may be unpublished
                    if (this.verbose) {
                        results.alerts.push({
                            severity: ALERT_SEVERITY.LOW,
                            type: 'DETAIL_FETCH_FAILED',
                            message: `Could not fetch details for "${pkg.name}": ${e.message}`,
                            affected: [pkg.name],
                        });
                    }
                }
            }
        } catch (e) {
            results.alerts.push({
                severity: ALERT_SEVERITY.HIGH,
                type: 'API_ERROR',
                message: `npm registry API error: ${e.message}`,
                affected: [],
            });
        }

        this.results.npm = results;
        this.alerts.push(...results.alerts);
        return results;
    }

    // ── GitHub Audit ───────────────────────────────────────────────
    async auditGithub(username) {
        if (!username) throw new Error('GitHub username is required');
        const results = { repos: [], alerts: [] };

        try {
            // Fetch public repos (paginate up to 300)
            let page = 1;
            let allRepos = [];
            while (page <= 3) {
                const res = await this._httpGet(
                    `https://api.github.com/users/${encodeURIComponent(username)}/repos?per_page=100&page=${page}&sort=updated`,
                    {
                        timeout: this.timeout,
                        headers: { 'Accept': 'application/vnd.github+json' },
                    }
                );
                if (!res.data || res.data.length === 0) break;
                allRepos = allRepos.concat(res.data);
                if (res.data.length < 100) break;
                page++;
            }

            for (const repo of allRepos) {
                const repoInfo = {
                    name: repo.name,
                    full_name: repo.full_name,
                    visibility: repo.private ? 'private' : 'public',
                    size_kb: repo.size,
                    fork: repo.fork,
                    description: repo.description || '',
                    default_branch: repo.default_branch,
                    updated_at: repo.updated_at,
                    html_url: repo.html_url,
                };
                results.repos.push(repoInfo);

                // Check for large repo size (potential node_modules committed)
                if (repo.size > 100000) { // 100MB in KB
                    results.alerts.push({
                        severity: ALERT_SEVERITY.MEDIUM,
                        type: 'LARGE_REPO',
                        message: `Repository "${repo.full_name}" is unusually large (${Math.round(repo.size / 1024)}MB) — may contain node_modules or binary files`,
                        affected: [repo.full_name],
                    });
                }

                // Check repo contents for suspicious files (top-level only)
                try {
                    const contentsRes = await this._httpGet(
                        `https://api.github.com/repos/${repo.full_name}/contents/`,
                        {
                            timeout: this.timeout,
                            headers: { 'Accept': 'application/vnd.github+json' },
                        }
                    );
                    if (Array.isArray(contentsRes.data)) {
                        const names = contentsRes.data.map(f => f.name);

                        if (names.includes('node_modules')) {
                            results.alerts.push({
                                severity: ALERT_SEVERITY.CRITICAL,
                                type: 'NODE_MODULES_COMMITTED',
                                message: `Repository "${repo.full_name}" has node_modules/ committed`,
                                affected: [repo.full_name],
                            });
                        }

                        for (const envFile of ['.env', '.env.local', '.env.production']) {
                            if (names.includes(envFile)) {
                                results.alerts.push({
                                    severity: ALERT_SEVERITY.CRITICAL,
                                    type: 'ENV_FILE_COMMITTED',
                                    message: `Repository "${repo.full_name}" has ${envFile} committed`,
                                    affected: [repo.full_name],
                                });
                            }
                        }

                        for (const keyFile of names.filter(n => n.endsWith('.key') || n.endsWith('.pem'))) {
                            results.alerts.push({
                                severity: ALERT_SEVERITY.CRITICAL,
                                type: 'KEY_FILE_COMMITTED',
                                message: `Repository "${repo.full_name}" has ${keyFile} committed`,
                                affected: [repo.full_name],
                            });
                        }
                    }
                } catch (e) {
                    // Contents fetch failed — empty repo or rate limited
                    if (this.verbose) {
                        results.alerts.push({
                            severity: ALERT_SEVERITY.LOW,
                            type: 'CONTENTS_FETCH_FAILED',
                            message: `Could not inspect contents of "${repo.full_name}": ${e.message}`,
                            affected: [repo.full_name],
                        });
                    }
                }
            }
        } catch (e) {
            results.alerts.push({
                severity: ALERT_SEVERITY.HIGH,
                type: 'API_ERROR',
                message: `GitHub API error: ${e.message}`,
                affected: [],
            });
        }

        this.results.github = results;
        this.alerts.push(...results.alerts);
        return results;
    }

    // ── ClawHub Audit ──────────────────────────────────────────────
    async auditClawHub(query) {
        if (!query) throw new Error('ClawHub search query is required');
        const results = { skills: [], alerts: [] };

        // Known malicious skill patterns (from IoC research)
        const KNOWN_MALICIOUS_PATTERNS = [
            'atomic-stealer', 'crypto-miner', 'reverse-shell',
            'claw-havoc', 'data-exfil', 'token-steal',
        ];

        try {
            // Try clawhub CLI first
            const output = execSync(`clawhub search "${query}" --json 2>/dev/null`, {
                timeout: this.timeout,
                encoding: 'utf-8',
            });
            const parsed = JSON.parse(output);
            if (Array.isArray(parsed)) {
                results.skills = parsed.map(s => ({
                    name: s.name || s.title,
                    author: s.author || 'unknown',
                    downloads: s.downloads || 0,
                    stars: s.stars || 0,
                    version: s.version || '0.0.0',
                    description: s.description || '',
                }));
            }
        } catch (e) {
            // clawhub CLI not available — graceful degradation
            results.alerts.push({
                severity: ALERT_SEVERITY.LOW,
                type: 'CLAWHUB_CLI_UNAVAILABLE',
                message: 'clawhub CLI not found — install with: npm install -g @anthropic-ai/clawhub',
                affected: [],
            });
        }

        // Check for known malicious patterns in results
        for (const skill of results.skills) {
            const lowerName = (skill.name || '').toLowerCase();
            const lowerDesc = (skill.description || '').toLowerCase();

            for (const pattern of KNOWN_MALICIOUS_PATTERNS) {
                if (lowerName.includes(pattern) || lowerDesc.includes(pattern)) {
                    results.alerts.push({
                        severity: ALERT_SEVERITY.CRITICAL,
                        type: 'KNOWN_MALICIOUS_SKILL',
                        message: `Skill "${skill.name}" matches known malicious pattern: ${pattern}`,
                        affected: [skill.name],
                    });
                }
            }

            // Suspicious DL/star ratio
            if (skill.downloads > 100 && skill.stars === 0) {
                results.alerts.push({
                    severity: ALERT_SEVERITY.MEDIUM,
                    type: 'SUSPICIOUS_DL_STAR_RATIO',
                    message: `Skill "${skill.name}" has ${skill.downloads} downloads but 0 stars — may indicate automated/suspicious usage`,
                    affected: [skill.name],
                });
            }
        }

        this.results.clawhub = results;
        this.alerts.push(...results.alerts);
        return results;
    }

    // ── Summary & Output ───────────────────────────────────────────
    getAlertCounts() {
        const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 };
        for (const alert of this.alerts) {
            counts[alert.severity] = (counts[alert.severity] || 0) + 1;
        }
        return counts;
    }

    getVerdict() {
        const counts = this.getAlertCounts();
        if (counts.CRITICAL > 0) return { label: 'CRITICAL EXPOSURE', exitCode: 2 };
        if (counts.HIGH > 0) return { label: 'HIGH RISK', exitCode: 1 };
        if (counts.MEDIUM > 0) return { label: 'NEEDS ATTENTION', exitCode: 0 };
        return { label: 'ALL CLEAR', exitCode: 0 };
    }

    printSummary() {
        if (this.quiet) return;
        const counts = this.getAlertCounts();
        const verdict = this.getVerdict();

        console.log('\n🛡️  guard-scanner asset audit');
        console.log('═'.repeat(50));

        if (this.results.npm) {
            console.log(`\n📦 npm: ${this.results.npm.packages.length} packages found`);
        }
        if (this.results.github) {
            console.log(`🐙 GitHub: ${this.results.github.repos.length} repositories found`);
        }
        if (this.results.clawhub) {
            console.log(`🦀 ClawHub: ${this.results.clawhub.skills.length} skills found`);
        }

        console.log(`\n📊 Alerts: ${counts.CRITICAL} CRITICAL | ${counts.HIGH} HIGH | ${counts.MEDIUM} MEDIUM | ${counts.LOW} LOW | ${counts.INFO} INFO`);
        console.log(`\n🏷️  Verdict: ${verdict.label}`);

        if (this.verbose && this.alerts.length > 0) {
            console.log('\n── Detailed Alerts ──');
            for (const alert of this.alerts) {
                const icon = alert.severity === 'CRITICAL' ? '🚨' :
                    alert.severity === 'HIGH' ? '⚠️' :
                        alert.severity === 'MEDIUM' ? '🔶' :
                            alert.severity === 'LOW' ? 'ℹ️' : '✅';
                console.log(`  ${icon} [${alert.severity}] ${alert.type}: ${alert.message}`);
            }
        }

        console.log('═'.repeat(50));
    }

    toJSON() {
        return {
            timestamp: new Date().toISOString(),
            scanner: `guard-scanner/${AUDIT_VERSION}`,
            type: 'asset-audit',
            results: this.results,
            alerts: this.alerts,
            counts: this.getAlertCounts(),
            verdict: this.getVerdict(),
        };
    }

    toSARIF() {
        const verdict = this.getVerdict();
        return {
            version: '2.1.0',
            $schema: 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json',
            runs: [{
                tool: {
                    driver: {
                        name: 'guard-scanner',
                        version: AUDIT_VERSION,
                        informationUri: 'https://github.com/koatora20/guard-scanner',
                        rules: this.alerts.map(a => ({
                            id: a.type,
                            shortDescription: { text: a.message },
                            defaultConfiguration: {
                                level: a.severity === 'CRITICAL' ? 'error' :
                                    a.severity === 'HIGH' ? 'error' :
                                        a.severity === 'MEDIUM' ? 'warning' : 'note',
                            },
                        })),
                    },
                },
                results: this.alerts.map(a => ({
                    ruleId: a.type,
                    level: a.severity === 'CRITICAL' ? 'error' :
                        a.severity === 'HIGH' ? 'error' :
                            a.severity === 'MEDIUM' ? 'warning' : 'note',
                    message: { text: a.message },
                    locations: a.affected.map(name => ({
                        physicalLocation: {
                            artifactLocation: { uri: name },
                        },
                    })),
                })),
            }],
        };
    }
}

export {  AssetAuditor, AUDIT_VERSION, ALERT_SEVERITY, httpGet  };
