import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * guard-scanner ClawHub Auto-Scanner
 * Fetches skills from ClawHub registry, scans each with guard-scanner,
 * and outputs a JSON report for the security dashboard.
 *
 * Usage:
 *   node scripts/scan-all.js                    # Scan top 50 skills
 *   node scripts/scan-all.js --limit 100        # Scan top 100
 *   node scripts/scan-all.js --query "security" # Search specific skills
 *   node scripts/scan-all.js --local ./skills   # Scan local skills dir
 *
 * Output: data/YYYY-MM-DD.json + data/latest.json
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: clawhub.ai (read-only skill registry)
 *   fs-read: [skill directories]
 *   fs-write: [data/ output directory]
 *   exec: [clawhub CLI, guard-scanner]
 *   purpose: Automated security scanning of public ClawHub skill registry
 */
'use strict';

import { execSync }  from 'child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

// ── Configuration ──
const DEFAULT_LIMIT = 50;
const DATA_DIR = path.join(__dirname, '..', 'data');
const SCAN_DIR = path.join(os.tmpdir(), 'guard-scanner-clawhub-scan');

// ── CLI Argument Parsing ──
function parseArgs() {
    const args = process.argv.slice(2);
    const opts = { limit: DEFAULT_LIMIT, query: '', local: null, verbose: false };
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--limit' && args[i + 1]) opts.limit = parseInt(args[++i], 10);
        if (args[i] === '--query' && args[i + 1]) opts.query = args[++i];
        if (args[i] === '--local' && args[i + 1]) opts.local = args[++i];
        if (args[i] === '--verbose' || args[i] === '-v') opts.verbose = true;
    }
    return opts;
}

// ── Skill Discovery ──
function discoverSkillsFromClawHub(query, limit) {
    console.log(`🔍 Searching ClawHub for skills... (limit: ${limit})`);
    try {
        const searchCmd = query
            ? `clawhub search "${query}" --json 2>/dev/null`
            : `clawhub search --json 2>/dev/null`;
        const output = execSync(searchCmd, { encoding: 'utf-8', timeout: 30000 });
        const skills = JSON.parse(output);
        return Array.isArray(skills) ? skills.slice(0, limit) : [];
    } catch {
        console.log('⚠️  clawhub CLI not available or search failed.');
        console.log('   Falling back to local skill scanning.');
        return [];
    }
}

function discoverLocalSkills(dir) {
    console.log(`📂 Scanning local skills directory: ${dir}`);
    const skills = [];
    if (!fs.existsSync(dir)) return skills;

    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const skillPath = path.join(dir, entry.name);
        const skillMd = path.join(skillPath, 'SKILL.md');
        if (fs.existsSync(skillMd)) {
            skills.push({
                slug: entry.name,
                name: entry.name,
                path: skillPath,
                source: 'local',
            });
        }
    }
    return skills;
}

// ── Scanning ──
// Detect guard-scanner CLI (global npm or local dev)
function getGuardScannerCmd() {
    try {
        execSync('guard-scanner --version', { encoding: 'utf-8', timeout: 5000, stdio: 'pipe' });
        return 'guard-scanner';
    } catch {
        // Fall back to local dev path
        const localCli = path.join(__dirname, '..', 'src', 'cli');
        if (fs.existsSync(localCli)) return `node "${localCli}"`;
        return 'npx -y @guava-parity/guard-scanner';
    }
}

const GS_CMD = getGuardScannerCmd();

function scanSkill(skillPath, skillName) {
    try {
        const result = execSync(
            `${GS_CMD} "${skillPath}" --json --strict --quiet 2>/dev/null`,
            { encoding: 'utf-8', timeout: 30000 }
        );
        const parsed = JSON.parse(result);
        return {
            name: skillName,
            path: skillPath,
            status: (parsed.findings || []).length === 0 ? 'clean' : 'findings',
            findingsCount: (parsed.findings || []).length,
            findings: parsed.findings || [],
            verdict: parsed.verdict || 'unknown',
            riskScore: parsed.riskScore || 0,
            scannedAt: new Date().toISOString(),
        };
    } catch (err) {
        // guard-scanner exits 1 on findings when --fail-on-findings
        // Try to parse the stdout as JSON
        if (err.stdout) {
            try {
                const parsed = JSON.parse(err.stdout);
                return {
                    name: skillName,
                    path: skillPath,
                    status: 'findings',
                    findingsCount: (parsed.findings || []).length,
                    findings: parsed.findings || [],
                    verdict: parsed.verdict || 'suspicious',
                    riskScore: parsed.riskScore || 0,
                    scannedAt: new Date().toISOString(),
                };
            } catch { /* fall through */ }
        }
        return {
            name: skillName,
            path: skillPath,
            status: 'error',
            findingsCount: 0,
            findings: [],
            verdict: 'error',
            riskScore: -1,
            error: err.message?.slice(0, 200) || 'Unknown error',
            scannedAt: new Date().toISOString(),
        };
    }
}

// ── Report Generation ──
function generateReport(results) {
    const totalSkills = results.length;
    const clean = results.filter(r => r.status === 'clean').length;
    const withFindings = results.filter(r => r.status === 'findings').length;
    const errors = results.filter(r => r.status === 'error').length;
    const totalFindings = results.reduce((sum, r) => sum + r.findingsCount, 0);

    // Category breakdown
    const categoryCount = {};
    for (const result of results) {
        for (const finding of result.findings) {
            const cat = finding.cat || finding.category || 'unknown';
            categoryCount[cat] = (categoryCount[cat] || 0) + 1;
        }
    }

    return {
        meta: {
            scanDate: new Date().toISOString(),
            scannerVersion: '12.5.0',
            totalSkills,
        },
        summary: {
            clean,
            withFindings,
            errors,
            totalFindings,
            cleanPercentage: totalSkills > 0 ? Math.round((clean / totalSkills) * 100) : 0,
        },
        categoryBreakdown: categoryCount,
        results: results.sort((a, b) => b.riskScore - a.riskScore), // Highest risk first
    };
}

// ── Main ──
async function main() {
    const opts = parseArgs();
    console.log('🛡️  guard-scanner ClawHub Auto-Scanner v12.5.0');
    console.log('═'.repeat(50));

    // Step 1: Discover skills
    let skills;
    if (opts.local) {
        skills = discoverLocalSkills(opts.local);
    } else {
        skills = discoverSkillsFromClawHub(opts.query, opts.limit);
        // If ClawHub unavailable, fall back to local workspace skills
        if (skills.length === 0) {
            const fallbackDirs = [
                path.join(os.homedir(), '.openclaw', 'workspace', 'skills'),
                path.join(os.homedir(), '.gemini', 'antigravity', 'skills'),
            ];
            for (const dir of fallbackDirs) {
                const local = discoverLocalSkills(dir);
                if (local.length > 0) {
                    skills = local;
                    break;
                }
            }
        }
    }

    console.log(`📋 Found ${skills.length} skills to scan`);
    if (skills.length === 0) {
        console.log('❌ No skills found. Use --local <dir> to scan a local directory.');
        process.exit(1);
    }

    // Step 2: Scan each skill
    const results = [];
    for (let i = 0; i < skills.length; i++) {
        const skill = skills[i];
        const skillPath = skill.path || skill.slug;
        const progress = `[${i + 1}/${skills.length}]`;

        if (opts.verbose) {
            process.stdout.write(`${progress} Scanning ${skill.name || skill.slug}...`);
        }

        const result = scanSkill(skillPath, skill.name || skill.slug);
        results.push(result);

        if (opts.verbose) {
            const icon = result.status === 'clean' ? '✅' :
                result.status === 'findings' ? '⚠️' : '❌';
            console.log(` ${icon} ${result.findingsCount} findings`);
        }
    }

    // Step 3: Generate report
    const report = generateReport(results);

    // Step 4: Save to data/
    fs.mkdirSync(DATA_DIR, { recursive: true });
    const dateStr = new Date().toISOString().split('T')[0];
    const datePath = path.join(DATA_DIR, `${dateStr}.json`);
    const latestPath = path.join(DATA_DIR, 'latest.json');

    fs.writeFileSync(datePath, JSON.stringify(report, null, 2));
    fs.writeFileSync(latestPath, JSON.stringify(report, null, 2));

    // Step 5: Print summary
    console.log('');
    console.log('═'.repeat(50));
    console.log('📊 Scan Complete!');
    console.log(`   Skills scanned: ${report.meta.totalSkills}`);
    console.log(`   ✅ Clean: ${report.summary.clean} (${report.summary.cleanPercentage}%)`);
    console.log(`   ⚠️  With findings: ${report.summary.withFindings}`);
    console.log(`   ❌ Errors: ${report.summary.errors}`);
    console.log(`   📝 Total findings: ${report.summary.totalFindings}`);
    console.log('');
    console.log(`   📁 Report: ${datePath}`);
    console.log(`   📁 Latest: ${latestPath}`);

    // Top 5 riskiest
    const risky = report.results.filter(r => r.riskScore > 0).slice(0, 5);
    if (risky.length > 0) {
        console.log('');
        console.log('🚨 Top 5 Riskiest Skills:');
        for (const r of risky) {
            console.log(`   ${r.riskScore.toFixed(1)} — ${r.name} (${r.findingsCount} findings)`);
        }
    }

    // Exit code: 0 if clean rate >= 50%, 1 otherwise
    process.exit(report.summary.cleanPercentage >= 50 ? 0 : 1);
}

main().catch(err => {
    console.error('Fatal error:', err.message);
    process.exit(1);
});
