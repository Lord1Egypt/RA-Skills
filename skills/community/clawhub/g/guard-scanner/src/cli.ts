// @ts-nocheck
/**
 * guard-scanner CLI
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: none
 *   fs-read: [scan target directory, plugin files, custom rules files]
 *   fs-write: [JSON/SARIF/HTML reports to scan directory]
 *   exec: none
 *   purpose: CLI entry point for guard-scanner static analysis
 *
 * Usage: guard-scanner [scan-dir] [options]
 *
 * Options:
 *   --verbose, -v       Detailed findings
 *   --json              JSON report
 *   --sarif             SARIF report (CI/CD)
 *   --html              HTML report
 *   --self-exclude      Skip scanning self
 *   --strict            Lower thresholds
 *   --summary-only      Summary only
 *   --check-deps        Scan dependencies
 *   --rules <file>      Custom rules JSON
 *   --plugin <file>     Load plugin module
 *   --fail-on-findings  Exit 1 on findings (CI/CD)
 *   --compliance <mode> Compliance projection (supported: owasp-asi)
 *   --help, -h          Help
 */

import fs  from 'fs';
import path  from 'path';
import { GuardScanner, VERSION  } from './scanner';
import { AssetAuditor, AUDIT_VERSION  } from './asset-auditor';
import { VTClient  } from './vt-client';
import { GuardWatcher  } from './watcher';
import { CIReporter  } from './ci-reporter';

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--version') || args.includes('-V')) {
    console.log(`guard-scanner v${VERSION} (audit v${AUDIT_VERSION})`);
    process.exit(0);
  }

  // ── serve subcommand (MCP server) ────────────────────────────
  if (args[0] === 'serve') {
    const { startServer } = await import('./mcp-server');
    startServer();
    return;
  }

  // ── benchmark subcommand ──────────────────────────────────────
  if (args[0] === 'benchmark') {
    const { buildBenchmarkLedger, buildFalsePositiveLedger, loadQualityContract, writeLedger } = await import('./benchmark-runner');
    const contract = loadQualityContract();
    const ledger = buildBenchmarkLedger(contract);
    const fpLedger = buildFalsePositiveLedger(ledger);
    const formatIdx = args.indexOf('--format');
    const formatValue = formatIdx >= 0 ? args[formatIdx + 1] : null;
    const writeLedgers = args.includes('--write-ledgers');

    if (args.includes('--help') || args.includes('-h')) {
      console.log(`
🛡️  guard-scanner benchmark — Detection Quality Ledger

Usage:
  guard-scanner benchmark
  guard-scanner benchmark --format json
  guard-scanner benchmark --write-ledgers

Options:
  --format json       Print benchmark ledger JSON to stdout
  --write-ledgers     Refresh docs/data/benchmark-ledger.json and fp-ledger.json
  --help, -h          Show this help
`);
      process.exit(0);
    }

    if (writeLedgers) {
      writeLedger(path.join(process.cwd(), 'docs', 'data', 'benchmark-ledger.json'), ledger);
      writeLedger(path.join(process.cwd(), 'docs', 'data', 'fp-ledger.json'), fpLedger);
    }

    if (formatValue === 'json') {
      process.stdout.write(JSON.stringify(ledger, null, 2) + '\n');
    } else {
      console.log(`🛡️  benchmark ${ledger.benchmark_version}`);
      for (const layer of ledger.layers) {
        console.log(`  • ${layer.layer}: benign=${layer.counts.benign}, malicious=${layer.counts.malicious}, precision=${layer.metrics.precision}, recall=${layer.metrics.recall}, fpr=${layer.metrics.false_positive_rate}, fnr=${layer.metrics.false_negative_rate}`);
      }
      console.log(`  • aggregate: precision=${ledger.aggregate.metrics.precision}, recall=${ledger.aggregate.metrics.recall}, fpr=${ledger.aggregate.metrics.false_positive_rate}, fnr=${ledger.aggregate.metrics.false_negative_rate}`);
      console.log(`  • explainability completeness=${ledger.explainability.rate}`);
    }

    process.exit(0);
  }

  // ── watch subcommand ──────────────────────────────────────────
  if (args[0] === 'watch') {
    const watchDir = args[1] || '.';
    const verbose = args.includes('--verbose') || args.includes('-v');
    const strict = args.includes('--strict');
    const soulLock = args.includes('--soul-lock');

    const watcher = new GuardWatcher({ verbose, strict, soulLock });

    process.on('SIGINT', () => {
      const stats = watcher.stop();
      console.log(`\n📊 Session: ${stats.scanCount} scans, ${stats.alertCount} alerts`);
      process.exit(0);
    });

    watcher.watch(watchDir);
    return;
  }

  // ── audit subcommand ──────────────────────────────────────────
  if (args[0] === 'audit') {
    const subCmd = args[1]; // npm | github | clawhub | all
    const target = args[2]; // username or query
    const verbose = args.includes('--verbose') || args.includes('-v');
    const formatIdx = args.indexOf('--format');
    const formatValue = formatIdx >= 0 ? args[formatIdx + 1] : null;
    const quiet = args.includes('--quiet') || !!formatValue;

    if (!subCmd || subCmd === '--help' || subCmd === '-h') {
      console.log(`
🛡️  guard-scanner audit v${AUDIT_VERSION} — Asset Audit Platform

Usage:
  guard-scanner audit npm <username>      Audit npm packages for leaks
  guard-scanner audit github <username>   Audit GitHub repos for exposure
  guard-scanner audit clawhub <query>     Audit ClawHub skills for threats
  guard-scanner audit all <username>      Run all audits

Options:
  --verbose, -v       Detailed alert output
  --format json|sarif Print report to stdout (pipeable)
  --quiet             Suppress text output
  --help, -h          Show this help

Examples:
  guard-scanner audit npm koatora20 --verbose
  guard-scanner audit github koatora20 --format json
  guard-scanner audit all koatora20 --verbose
`);
      process.exit(0);
    }

    if (!target && subCmd !== 'all') {
      console.error(`❌ Usage: guard-scanner audit ${subCmd} <username>`);
      process.exit(2);
    }

    const vtScan = args.includes('--vt-scan');
    let vtClient = null;
    if (vtScan) {
      const vtKey = process.env.VT_API_KEY;
      if (!vtKey) { console.error('❌ --vt-scan requires VT_API_KEY environment variable'); process.exit(2); }
      vtClient = new VTClient(vtKey, { verbose });
    }

    const auditor = new AssetAuditor({ verbose, format: formatValue, quiet, vtClient });

    try {
      if (subCmd === 'npm' || subCmd === 'all') {
        await auditor.auditNpm(target);
      }
      if (subCmd === 'github' || subCmd === 'all') {
        await auditor.auditGithub(target);
      }
      if (subCmd === 'clawhub' || subCmd === 'all') {
        await auditor.auditClawHub(target);
      }

      if (!['npm', 'github', 'clawhub', 'all'].includes(subCmd)) {
        console.error(`❌ Unknown audit target: ${subCmd}. Use: npm, github, clawhub, or all`);
        process.exit(2);
      }

      // Output
      if (formatValue === 'json') {
        process.stdout.write(JSON.stringify(auditor.toJSON(), null, 2) + '\n');
      } else if (formatValue === 'sarif') {
        process.stdout.write(JSON.stringify(auditor.toSARIF(), null, 2) + '\n');
      } else {
        auditor.printSummary();
      }

      const verdict = auditor.getVerdict();
      process.exit(verdict.exitCode);
    } catch (e) {
      console.error(`❌ Audit error: ${e.message}`);
      process.exit(2);
    }
    return;
  }

  // ── crawl subcommand ──────────────────────────────────────────
  if (args[0] === 'crawl') {
    const { SkillCrawler } = await import('./skill-crawler');
    const subCmd = args[1]; // clawhub | github | url
    const target = args[2]; // query or URL
    const verbose = args.includes('--verbose') || args.includes('-v');
    const formatIdx = args.indexOf('--format');
    const formatValue = formatIdx >= 0 ? args[formatIdx + 1] : null;
    const quiet = !!formatValue;
    const maxIdx = args.indexOf('--max');
    const maxSkills = maxIdx >= 0 ? parseInt(args[maxIdx + 1], 10) : 50;

    if (!subCmd || subCmd === '--help' || subCmd === '-h') {
      console.log(`
🛡️  guard-scanner crawl — Autonomous Skill Scanner

Usage:
  guard-scanner crawl clawhub              Crawl ClawHub for all SKILL.md
  guard-scanner crawl github <query>       Search GitHub for SKILL.md
  guard-scanner crawl url <url>            Scan a single SKILL.md URL

Options:
  --verbose, -v       Show detection details
  --format json       Output JSON to stdout
  --max <n>           Max skills to scan (default: 50)
  --help, -h          Show this help

Examples:
  guard-scanner crawl clawhub --verbose
  guard-scanner crawl github "polymarket trader" --format json
  guard-scanner crawl url https://raw.githubusercontent.com/.../SKILL.md
`);
      process.exit(0);
    }

    const crawler = new SkillCrawler({ verbose, quiet, concurrency: 5 });

    try {
      if (subCmd === 'clawhub') {
        await crawler.crawlClawHub({ maxSkills });
      } else if (subCmd === 'github') {
        if (!target) { console.error('❌ Usage: guard-scanner crawl github <query>'); process.exit(2); }
        await crawler.crawlGitHub(target, { maxResults: maxSkills });
      } else if (subCmd === 'url') {
        if (!target) { console.error('❌ Usage: guard-scanner crawl url <url>'); process.exit(2); }
        await crawler.scanUrl(target, target);
      } else {
        console.error(`❌ Unknown crawl target: ${subCmd}. Use: clawhub, github, or url`);
        process.exit(2);
      }

      if (formatValue === 'json') {
        process.stdout.write(JSON.stringify(crawler.toJSON(), null, 2) + '\n');
      } else {
        crawler.printSummary();
      }

      const summary = crawler.getSummary();
      process.exit(summary.unsafe > 0 ? 1 : 0);
    } catch (e) {
      console.error(`❌ Crawl error: ${e.message}`);
      process.exit(2);
    }
    return;
  }

  // ── patrol subcommand ──────────────────────────────────────────
  if (args[0] === 'patrol') {
    const { SkillCrawler } = await import('./skill-crawler');
    const verbose = args.includes('--verbose') || args.includes('-v');
    const once = args.includes('--once');
    const intervalIdx = args.indexOf('--interval');
    const intervalSecs = intervalIdx >= 0 ? parseInt(args[intervalIdx + 1], 10) : 3600;
    const formatIdx = args.indexOf('--format');
    const formatValue = formatIdx >= 0 ? args[formatIdx + 1] : null;

    if (args.includes('--help') || args.includes('-h')) {
      console.log(`
🛡️  guard-scanner patrol — Autonomous Security Patrol

Usage:
  guard-scanner patrol --once              Run one patrol cycle
  guard-scanner patrol --interval 3600     Patrol every N seconds

Options:
  --once              Run once and exit
  --interval <secs>   Polling interval (default: 3600 = 1 hour)
  --verbose, -v       Show detection details
  --format json       Output JSON
  --help, -h          Show this help
`);
      process.exit(0);
    }

    async function runPatrol() {
      const timestamp = new Date().toISOString();
      console.log(`\n🚨 Patrol cycle starting at ${timestamp}`);
      console.log('─'.repeat(54));

      const crawler = new SkillCrawler({ verbose, quiet: !!formatValue, concurrency: 5 });
      await crawler.crawlClawHub({ maxSkills: 50 });

      if (formatValue === 'json') {
        process.stdout.write(JSON.stringify(crawler.toJSON(), null, 2) + '\n');
      } else {
        crawler.printSummary();
      }

      const summary = crawler.getSummary();
      if (summary.unsafe > 0) {
        console.log(`\n⚠️  ${summary.unsafe} unsafe skill(s) detected!`);
      }
      return summary;
    }

    try {
      if (once) {
        const summary = await runPatrol();
        process.exit(summary.unsafe > 0 ? 1 : 0);
      } else {
        console.log(`🛡️  guard-scanner patrol mode — interval: ${intervalSecs}s`);
        console.log(`   Press Ctrl+C to stop\n`);
        await runPatrol();
        setInterval(async () => {
          await runPatrol();
        }, intervalSecs * 1000);
      }
    } catch (e) {
      console.error(`❌ Patrol error: ${e.message}`);
      process.exit(2);
    }
    return;
  }

  // ── existing scan logic (backward compatible) ─────────────────

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🛡️  guard-scanner v${VERSION} — Agent Skill Security Scanner

Usage: guard-scanner [scan-dir] [options]
       guard-scanner serve              Start as MCP server (stdio)
       guard-scanner benchmark          Generate benchmark/fp ledgers
       guard-scanner audit <npm|github|clawhub|all> <username> [options]

Options:
  --verbose, -v       Detailed findings with categories and samples
  --json              Write JSON report to file
  --sarif             Write SARIF report to file (GitHub Code Scanning / CI/CD)
  --html              Write HTML report (visual dashboard)
  --format json|sarif Print JSON or SARIF to stdout (pipeable, v3.2.0)
  --quiet             Suppress all text output (use with --format for clean pipes)
  --self-exclude      Skip scanning the guard-scanner skill itself
  --strict            Lower detection thresholds (more sensitive)
  --summary-only      Only print the summary table
  --check-deps        Scan package.json for dependency chain risks
  --soul-lock         Enable Soul Lock patterns (agent identity protection)
  --rules <file>      Load custom rules from JSON file
  --plugin <file>     Load plugin module (JS file exporting { name, patterns })
  --fail-on-findings  Exit code 1 if any findings (CI/CD)
  --help, -h          Show this help
  --version, -V       Show version

Custom Rules JSON Format:
  [
    {
      "id": "CUSTOM_001",
      "pattern": "dangerous_function\\\\(",
      "flags": "gi",
      "severity": "HIGH",
      "cat": "malicious-code",
      "desc": "Custom: dangerous function call",
      "codeOnly": true
    }
  ]

Plugin API:
  // my-plugin.js
  export default {
    name: 'my-plugin',
    patterns: [
      { id: 'MY_01', cat: 'custom', regex: /pattern/g, severity: 'HIGH', desc: 'Description', all: true }
    ]
  };

Examples:
  guard-scanner ./skills/ --verbose --self-exclude
  guard-scanner ./skills/ --strict --json --sarif --check-deps
  guard-scanner ./skills/ --html --verbose --check-deps
  guard-scanner ./skills/ --rules my-rules.json --fail-on-findings
  guard-scanner ./skills/ --plugin ./my-plugin.js
`);
    process.exit(0);
  }

  const verbose = args.includes('--verbose') || args.includes('-v');
  const jsonOutput = args.includes('--json');
  const sarifOutput = args.includes('--sarif');
  const htmlOutput = args.includes('--html');
  const selfExclude = args.includes('--self-exclude');
  const strict = args.includes('--strict');
  const summaryOnly = args.includes('--summary-only');
  const checkDeps = args.includes('--check-deps');
  const soulLock = args.includes('--soul-lock');
  const failOnFindings = args.includes('--fail-on-findings');
  const quietMode = args.includes('--quiet');
  const complianceIdx = args.indexOf('--compliance');
  const compliance = complianceIdx >= 0 ? args[complianceIdx + 1] : null;

  // --format json|sarif → stdout output (v3.2.0)
  const formatIdx = args.indexOf('--format');
  const formatValue = formatIdx >= 0 ? args[formatIdx + 1] : null;

  const rulesIdx = args.indexOf('--rules');
  const rulesFile = rulesIdx >= 0 ? args[rulesIdx + 1] : null;

  // Collect plugins
  const plugins: string[] = [];
  let idx = 0;
  while (idx < args.length) {
    if (args[idx] === '--plugin' && args[idx + 1]) {
      plugins.push(args[idx + 1]);
      idx += 2;
    } else {
      idx++;
    }
  }

  const scanDir = args.find(a =>
    !a.startsWith('-') &&
    a !== rulesFile &&
    a !== formatValue &&
    a !== compliance &&
    !plugins.includes(a)
  ) || process.cwd();

  try {
    const scanner = new GuardScanner({
      verbose, selfExclude, strict, summaryOnly, checkDeps, soulLock, rulesFile, plugins, compliance,
      quiet: quietMode || !!formatValue,
    });

    scanner.scanDirectory(scanDir);

    // Output reports (file-based, backward compatible)
    if (jsonOutput) {
      const report = scanner.toJSON();
      const outPath = path.join(scanDir, 'guard-scanner-report.json');
      fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
      if (!quietMode && !formatValue) console.log(`\n📄 JSON report: ${outPath}`);
    }

    if (sarifOutput) {
      const outPath = path.join(scanDir, 'guard-scanner.sarif');
      fs.writeFileSync(outPath, JSON.stringify(scanner.toSARIF(scanDir), null, 2));
      if (!quietMode && !formatValue) console.log(`\n📄 SARIF report: ${outPath}`);
    }

    if (htmlOutput) {
      const outPath = path.join(scanDir, 'guard-scanner-report.html');
      fs.writeFileSync(outPath, scanner.toHTML());
      if (!quietMode && !formatValue) console.log(`\n📄 HTML report: ${outPath}`);
    }

    // --format stdout output (v3.2.0)
    if (formatValue === 'json') {
      process.stdout.write(JSON.stringify(scanner.toJSON(), null, 2) + '\n');
    } else if (formatValue === 'sarif') {
      process.stdout.write(JSON.stringify(scanner.toSARIF(scanDir), null, 2) + '\n');
    } else if (formatValue) {
      console.error(`❌ Unknown format: ${formatValue}. Use 'json' or 'sarif'.`);
      process.exit(2);
    }

    // Exit codes
    if (scanner.stats.malicious > 0) process.exit(1);
    if (failOnFindings && scanner.findings.length > 0) process.exit(1);
    process.exit(0);
  } catch (error) {
    console.error(`❌ ${error.message}`);
    process.exit(2);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
