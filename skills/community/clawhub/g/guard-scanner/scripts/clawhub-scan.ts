import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * ClawHub Dashboard Data Generator
 *
 * Phase 1: Metadata-based risk analysis (fast, <30s)
 *   - DL/star ratio anomalies
 *   - Suspicious naming patterns
 *   - Known malicious skill names from IoC research
 *   - Age-based risk scoring
 *
 * Phase 2 (GitHub Actions cron): Deep SKILL.md scanning
 *
 * Usage: node scripts/clawhub-scan.js [--limit N] [--sort newest|installs|downloads]
 */

import { execSync }  from 'child_process';
import fs from 'node:fs';
import path from 'node:path';
import { PATTERNS }  from '../src/patterns';

const VERSION = JSON.parse(
    fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8')
).version;

const args = process.argv.slice(2);
const limitIdx = args.indexOf('--limit');
const limit = limitIdx >= 0 ? parseInt(args[limitIdx + 1], 10) : 200;
const sortIdx = args.indexOf('--sort');
const sort = sortIdx >= 0 ? args[sortIdx + 1] : 'newest';
const outDir = path.join(__dirname, '..', 'docs', 'data');

console.log(`🛡️  ClawHub Dashboard Scanner — v${VERSION}`);
console.log(`   Patterns: ${PATTERNS.length} | Limit: ${limit} | Sort: ${sort}\n`);

// ── Known malicious patterns from IoC research ──
const MALICIOUS_NAMES = [
    'atomic-stealer', 'crypto-miner', 'reverse-shell', 'claw-havoc',
    'data-exfil', 'token-steal', 'keylogger', 'rootkit', 'backdoor',
    'ransomware', 'cryptojack', 'botnet', 'trojan', 'spyware',
    'stealer', 'c2-beacon', 'phishing-kit', 'credential-harvest',
];

const SUSPICIOUS_NAME_PATTERNS = [
    /^[a-z]{1,3}-[a-z]{1,3}$/,           // very short nonsense slugs
    /(?:free|crack|keygen|hack|exploit)/i, // known bait words
    /(?:test|asdf|qwerty|aaa|xxx)/i,       // test junk
    /(?:\d{6,})/,                          // long number sequences
];

// ── Fetch all skills (6 sorts + keyword searches) ──
console.log('📡 Fetching ClawHub registry (full coverage mode)...');
const startTime = Date.now();
let allSkills = [];
const slugSet = new Set();

function addSkills(items) {
    for (const item of items) {
        if (!slugSet.has(item.slug)) {
            slugSet.add(item.slug);
            allSkills.push(item);
        }
    }
}

// Phase 1: All 6 explore sort orders
const SORTS = ['newest', 'downloads', 'rating', 'installs', 'installsAllTime', 'trending'];
for (const s of SORTS) {
    try {
        const raw = execSync(`clawhub explore --limit ${limit} --sort ${s} --json 2>/dev/null`, {
            encoding: 'utf-8', timeout: 30000,
        });
        const data = JSON.parse(raw);
        addSkills(data.items || []);
        process.stdout.write(`\r   explore/${s}: ${(data.items || []).length} fetched → ${allSkills.length} unique`);
    } catch { /* skip */ }
}
console.log('');

// Phase 2: Search queries (text output parsing — no --json support)
const SEARCH_QUERIES = [
    'security', 'database', 'api', 'file', 'web', 'image', 'audio',
    'email', 'calendar', 'chat', 'code', 'deploy', 'test', 'monitor',
    'ai', 'llm', 'agent', 'tool', 'browser', 'search', 'data',
    'automation', 'workflow', 'devops', 'cloud', 'docker', 'kubernetes',
    'slack', 'discord', 'notion', 'jira', 'aws', 'gcp', 'python',
    'webhook', 'scraper', 'crawler', 'pdf', 'video', 'music',
    'crypto', 'blockchain', 'payment', 'auth', 'oauth', 'sso',
    'cms', 'wordpress', 'shopify', 'stripe', 'twilio', 'github',
];
let searchAdded = 0;
for (const q of SEARCH_QUERIES) {
    try {
        const raw = execSync(`clawhub search "${q}" --limit 50 2>/dev/null`, {
            encoding: 'utf-8', timeout: 15000,
        });
        // Parse: "slug  DisplayName  (score)\n"
        const lines = raw.split('\n').filter(l => l.includes('(') && !l.startsWith('-'));
        for (const line of lines) {
            const match = line.match(/^(\S+)\s+(.+?)\s+\([\d.]+\)$/);
            if (match && !slugSet.has(match[1])) {
                slugSet.add(match[1]);
                allSkills.push({
                    slug: match[1],
                    displayName: match[2].trim(),
                    summary: '',
                    stats: { downloads: 0, installs: 0, installsAllTime: 0, stars: 0 },
                });
                searchAdded++;
            }
        }
    } catch { /* skip */ }
}
if (searchAdded > 0) console.log(`   +${searchAdded} from search queries`);

// Phase 3: Direct API pagination (clawhub.ai) — free tier only
const API_BASE = 'https://clawhub.ai/api/v1/skills';
for (let page = 1; page <= 5; page++) {
    try {
        const raw = execSync(
            `curl -s "${API_BASE}?limit=200&page=${page}&sort=newest" 2>/dev/null`,
            { encoding: 'utf-8', timeout: 15000 }
        );
        if (raw.includes('Rate limit')) break;
        const data = JSON.parse(raw);
        const items = data.items || data.skills || [];
        if (items.length === 0) break;
        let added = 0;
        for (const item of items) {
            const sk = item.slug || item.name;
            if (sk && !slugSet.has(sk)) {
                slugSet.add(sk);
                allSkills.push({
                    slug: sk,
                    displayName: item.displayName || item.name || sk,
                    summary: item.summary || item.description || '',
                    stats: item.stats || { downloads: 0, installs: 0, installsAllTime: 0, stars: 0 },
                });
                added++;
            }
        }
        if (added > 0) console.log(`   +${added} from API page ${page}`);
        if (items.length < 200) break; // last page
    } catch { break; }
}

console.log(`   Total unique skills: ${allSkills.length}\n`);

// ── Analyze each skill ──
const results = [];
const categoryBreakdown = {};
let totalFindings = 0;
let cleanCount = 0;

for (const skill of allSkills) {
    const slug = skill.slug;
    const name = (skill.displayName || slug).toLowerCase();
    const summary = (skill.summary || '').toLowerCase();
    const downloads = skill.stats?.downloads || 0;
    const stars = skill.stats?.stars || 0;
    const installs = skill.stats?.installsAllTime || 0;
    const findings = [];

    // ── Risk checks ──

    // 1. Known malicious name match
    for (const mal of MALICIOUS_NAMES) {
        if (name.includes(mal) || slug.includes(mal) || summary.includes(mal)) {
            findings.push({
                id: 'KNOWN_MALICIOUS_NAME', cat: 'supply-chain-v2',
                severity: 'CRITICAL', desc: `Known malicious pattern in name: "${mal}"`,
            });
        }
    }

    // 2. Suspicious naming
    for (const pat of SUSPICIOUS_NAME_PATTERNS) {
        if (pat.test(slug)) {
            findings.push({
                id: 'SUSPICIOUS_SLUG', cat: 'obfuscation',
                severity: 'MEDIUM', desc: `Suspicious skill slug pattern: "${slug}"`,
            });
            break;
        }
    }

    // 3. DL/star ratio anomaly (high DL, zero stars = bot/suspicious)
    if (downloads > 500 && stars === 0) {
        findings.push({
            id: 'ANOMALY_DL_NO_STARS', cat: 'autonomous-risk',
            severity: 'MEDIUM', desc: `${downloads} downloads but 0 stars — possible automated/bot usage`,
        });
    }

    // 4. Zero installs but high DL (scraping/crawling activity)
    if (downloads > 100 && installs === 0) {
        findings.push({
            id: 'ANOMALY_DL_NO_INSTALLS', cat: 'data-flow',
            severity: 'LOW', desc: `${downloads} downloads but 0 installs — possible scraping`,
        });
    }

    // 5. Summary contains suspicious keywords
    const suspiciousKeywords = [
        /(?:exec|eval|system|child_process|spawn)\s*\(/i,
        /(?:api[_-]?key|secret|password|token)\s*[:=]/i,
        /(?:chmod\s+\+s|sudo\s+rm|curl.*\|\s*(?:bash|sh))/i,
        /(?:reverse.?shell|bind.?shell|nc\s+-l)/i,
    ];
    for (const kw of suspiciousKeywords) {
        if (kw.test(summary)) {
            findings.push({
                id: 'SUSPICIOUS_SUMMARY', cat: 'malicious-code',
                severity: 'HIGH', desc: `Suspicious keyword in skill summary`,
            });
            break;
        }
    }

    // 6. Run subset of PATTERNS against summary text (doc-safe patterns only)
    for (const p of PATTERNS) {
        if (p.codeOnly) continue; // skip code-only patterns
        const re = new RegExp(p.regex.source, p.regex.flags);
        if (re.test(summary)) {
            findings.push({
                id: p.id, cat: p.cat, severity: p.severity, desc: p.desc,
            });
        }
    }

    // Deduplicate findings by ID
    const seen = new Set();
    const unique = findings.filter(f => {
        if (seen.has(f.id)) return false;
        seen.add(f.id);
        return true;
    });

    totalFindings += unique.length;
    for (const f of unique) {
        categoryBreakdown[f.cat] = (categoryBreakdown[f.cat] || 0) + 1;
    }

    const riskScore = unique.length === 0 ? 0 :
        Math.min(100, unique.length * 10 +
            unique.filter(f => f.severity === 'CRITICAL').length * 30 +
            unique.filter(f => f.severity === 'HIGH').length * 15);

    results.push({
        name: skill.displayName || slug,
        slug,
        author: 'registry',
        downloads, installs, stars,
        status: unique.length > 0 ? 'findings' : 'clean',
        findingsCount: unique.length,
        riskScore,
        findings: unique.slice(0, 10),
        scannedAt: new Date().toISOString(),
    });

    if (unique.length === 0) cleanCount++;
}

const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

// ── Dashboard JSON ──
const withFindings = results.filter(r => r.status === 'findings').length;
const totalSkills = results.length;
const cleanPct = totalSkills > 0 ? Math.round(cleanCount / totalSkills * 100) : 0;

const catLabels = {
    'prompt-injection': 'Prompt Injection', 'malicious-code': 'Malicious Code',
    'exfiltration': 'Exfiltration', 'memory-poisoning': 'Memory Poisoning',
    'mcp-security': 'MCP Security', 'credential-handling': 'Credential Handling',
    'obfuscation': 'Obfuscation', 'identity-hijack': 'Identity Hijack',
    'persistence': 'Persistence', 'cve-patterns': 'CVE Patterns',
    'a2a-contagion': 'A2A Contagion', 'agent-protocol': 'Agent Protocol',
    'autonomous-risk': 'Autonomous Risk', 'config-impact': 'Config Impact',
    'safeguard-bypass': 'Safeguard Bypass', 'supply-chain-v2': 'Supply Chain',
    'data-flow': 'Data Flow', 'leaky-skills': 'Leaky Skills',
    'secret-detection': 'Secret Detection',
};

const readableCatBreakdown = {};
for (const [cat, count] of Object.entries(categoryBreakdown)
    .sort((a, b) => b[1] - a[1])) {
    readableCatBreakdown[catLabels[cat] || cat] = count;
}

const dashboardData = {
    meta: {
        scanDate: new Date().toISOString(),
        scannerVersion: VERSION,
        totalSkills,
        patternCount: PATTERNS.length,
        source: 'ClawHub Registry',
        scanMode: 'metadata + summary pattern matching',
        elapsed: `${elapsed}s`,
    },
    summary: {
        clean: cleanCount,
        withFindings,
        errors: 0,
        totalFindings,
        cleanPercentage: cleanPct,
    },
    categoryBreakdown: readableCatBreakdown,
    results: results.sort((a, b) => b.riskScore - a.riskScore),
};

fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, 'latest.json');
fs.writeFileSync(outPath, JSON.stringify(dashboardData, null, 2));

console.log('═══════════════════════════════════════════');
console.log(`🛡️  ClawHub Scan Complete (${elapsed}s)`);
console.log(`   Skills analyzed: ${totalSkills}`);
console.log(`   ✅ Clean:        ${cleanCount} (${cleanPct}%)`);
console.log(`   ⚠️  Findings:    ${withFindings}`);
console.log(`   Total findings:  ${totalFindings}`);
console.log(`   Categories hit:  ${Object.keys(categoryBreakdown).length}`);
console.log(`\n📄 ${outPath}`);
console.log('═══════════════════════════════════════════');
