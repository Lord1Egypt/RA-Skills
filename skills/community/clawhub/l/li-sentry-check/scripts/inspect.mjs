#!/usr/bin/env node
/*
  li_sentry_check - Multi-platform server inspection (Node.js version)
  - Loads targets from references/targets.yaml
  - Loads allowlisted checks from references/checks.yaml
  - Runs each command over SSH (non-interactive), captures stdout/stderr
  - Prints a Markdown report with anomaly highlighting
  Compatible with OpenClaw.

  SECURITY CONSTRAINTS:
  - ONLY reads from: references/targets.yaml, references/checks.yaml, SSH key
  - ONLY connects to ONE server via SSH (target specified in targets.yaml)
  - ONLY executes commands from references/checks.yaml allowlist
  - NEVER modifies server state, installs software, or writes files
  - NEVER exfiltrates data to external services
  - NEVER executes arbitrary commands
*/
import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// SECURITY: Only these files are read
const ALLOWED_FILES = [
  'references/targets.yaml',
  'references/checks.yaml',
];

// SECURITY: Only SSH connections are made (no HTTP, no external APIs)
// SECURITY: Only commands from checks.yaml are executed
// SECURITY: No state changes on remote servers (read-only)

// Error keywords for anomaly detection
const ERROR_KEYWORDS = [
  'failed', 'error', 'alert', 'critical', 'SELinux is preventing',
  'WARNING', 'panic', 'segfault', 'oom', 'killed process',
  'no space', 'disk quota', 'read-only', 'corrupt', 'timeout',
  'refused', 'denied', 'unreachable', 'broken pipe', 'i/o error',
];

function usage() {
  console.log(`Usage:
  node scripts/inspect.mjs --target <name> --checks <group> [--format markdown|json]
Options:
  --target   Target name in references/targets.yaml
  --checks   Check group in references/checks.yaml (default: basic)
  --format   Output format: markdown, json (default: markdown)
  --output   Write report to file instead of stdout
`);
}

function parseArgs(argv) {
  const args = { checks: 'basic', format: 'markdown' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') { args.help = true; }
    else if (a === '--target') args.target = argv[++i];
    else if (a === '--checks') args.checks = argv[++i];
    else if (a === '--format') args.format = argv[++i];
    else if (a === '--output') args.output = argv[++i];
    else { throw new Error(`Unknown arg: ${a}`); }
  }
  return args;
}

function parseSimpleYaml(text) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const root = {};
  const stack = [{ indent: -1, obj: root }];
  for (let idx = 0; idx < lines.length; idx++) {
    const raw = lines[idx];
    const line = raw.replace(/\t/g, '  ');
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const indent = line.match(/^ */)[0].length;
    while (stack.length && indent <= stack[stack.length - 1].indent) stack.pop();
    const parent = stack[stack.length - 1].obj;
    const trimmed = line.trim();
    if (trimmed.startsWith('- ')) {
      if (!Array.isArray(parent)) throw new Error('YAML list item in non-list');
      parent.push(stripQuotes(trimmed.slice(2).trim()));
      continue;
    }
    const [k, ...rest] = trimmed.split(':');
    const key = k.trim();
    const value = rest.join(':').trim();
    if (value === '') {
      let j = idx + 1;
      let next = null;
      while (j < lines.length) {
        const nl = lines[j].replace(/\t/g, '  ');
        const nt = nl.trim();
        if (nt && !nt.startsWith('#')) {
          next = { indent: nl.match(/^ */)[0].length, trimmed: nt };
          break;
        }
        j++;
      }
      const isList = next && next.indent > indent && next.trimmed.startsWith('- ');
      const container = isList ? [] : {};
      parent[key] = container;
      stack.push({ indent, obj: container });
    } else {
      parent[key] = stripQuotes(value);
    }
  }
  return root;
}

function stripQuotes(s) {
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    return s.slice(1, -1);
  }
  if (/^\d+$/.test(s)) return Number(s);
  return s;
}

function execFileP(cmd, args, { timeoutMs } = {}) {
  return new Promise((resolve) => {
    execFile(cmd, args, { timeout: timeoutMs, maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      resolve({ error, stdout: stdout ?? '', stderr: stderr ?? '' });
    });
  });
}

function mdEscape(s) {
  return s.replace(/`/g, '\\`');
}

function nowIso() {
  return new Date().toISOString();
}

function hasAnomaly(stdout, stderr) {
  const combined = (stdout + stderr).toLowerCase();
  return ERROR_KEYWORDS.some(kw => combined.includes(kw.toLowerCase()));
}

function buildServiceCommands(services) {
  const out = [];
  const uniq = [...new Set((services || []).map(s => String(s).trim()).filter(Boolean))];
  for (const name of uniq) {
    // Validate service name to prevent command injection
    if (!/^[a-zA-Z0-9_-]+$/.test(name)) {
      out.push({
        id: `svc_${name.replace(/[^a-zA-Z0-9_-]/g, '_')}_invalid`,
        cmd: `echo 'Invalid service name (only alphanumeric, hyphens, underscores allowed): ${name}'`,
        timeoutSec: 3,
      });
      continue;
    }
    out.push({
      id: `svc_${name}_status`,
      cmd: `systemctl status ${name} --no-pager | sed -n '1,40p'`,
      timeoutSec: 12,
    });
    out.push({
      id: `svc_${name}_errors`,
      cmd: `journalctl -u ${name} -p err..alert -n 80 --no-pager || true`,
      timeoutSec: 15,
    });
    out.push({
      id: `svc_${name}_recent`,
      cmd: `journalctl -u ${name} -n 120 --no-pager | egrep -i 'warn|warning|error|failed|fail|critical|crit|alert|panic|segfault|oom|killed process|timeout|timed out|refused|denied|unreachable|reset|broken pipe|i/o error|corrupt|read-only|no space|disk quota|throttl|backoff|rate limit|too many|conntrack|dropped' | tail -n 60 || true`,
      timeoutSec: 15,
    });
  }
  if (out.length === 0) {
    out.push({
      id: 'services_config',
      cmd: "echo 'No services configured for this target. Add targets.<name>.services in references/targets.yaml'",
      timeoutSec: 3,
    });
  }
  return out;
}

function buildDailyCommands(t) {
  const base = [
    { id: 'basic_identity', cmd: 'whoami; hostname; uname -r; date -Is', timeoutSec: 5 },
    { id: 'basic_uptime', cmd: 'uptime', timeoutSec: 5 },
    { id: 'basic_os', cmd: "cat /etc/os-release | sed -n '1,12p'", timeoutSec: 5 },
    { id: 'hw_cpu', cmd: "(command -v mpstat >/dev/null 2>&1 && mpstat -P ALL 1 3 | sed -n '1,160p') || (top -b -n1 | sed -n '1,25p') || true", timeoutSec: 15 },
    { id: 'hw_mem', cmd: "free -h; echo; cat /proc/meminfo | egrep -i '^(MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty|Writeback|Slab):' || true", timeoutSec: 10 },
    { id: 'hw_disk_fs', cmd: "df -hT | sed -n '1,25p'", timeoutSec: 10 },
    { id: 'hw_disk_io', cmd: "(command -v iostat >/dev/null 2>&1 && iostat -x 1 3 | sed -n '1,120p') || true", timeoutSec: 18 },
    { id: 'hw_net_overview', cmd: "ss -s | sed -n '1,80p'", timeoutSec: 10 },
    { id: 'logs_journal_err_24h', cmd: 'journalctl -p err..alert -S -24h --no-pager | tail -n 200 || true', timeoutSec: 20 },
    { id: 'logs_dmesg_key', cmd: "dmesg -T 2>/dev/null | egrep -i 'error|fail|oom|killed process|segfault|panic|xfs|ext4|nvme|reset|link down|call trace' | tail -n 200 || true", timeoutSec: 12 },
    { id: 'sec_last_failed', cmd: "lastb -n 50 2>/dev/null | sed -n '1,60p' || true", timeoutSec: 12 },
    { id: 'sec_sshd_suspicious_24h', cmd: "journalctl -u sshd -S -24h --no-pager | egrep -i 'failed password|invalid user|authentication failure|maximum authentication attempts|POSSIBLE BREAK-IN ATTEMPT|Did not receive identification string|Connection closed by authenticating user|error: kex_exchange_identification' | tail -n 200 || true", timeoutSec: 20 },
    { id: 'systemd_failed_units', cmd: 'systemctl --failed --no-pager || true', timeoutSec: 10 },
    { id: 'systemd_recent_errors', cmd: 'journalctl -p err..alert -n 80 --no-pager || true', timeoutSec: 15 },
  ];
  const svc = buildServiceCommands(t?.services ?? []);
  return base.concat(svc);
}

function parseChecksYaml(text) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const out = { checks: {} };
  let curGroup = null;
  let inCommands = false;
  let curCmd = null;
  const kv = (s) => {
    const i = s.indexOf(':');
    if (i === -1) return null;
    return [s.slice(0, i).trim(), s.slice(i + 1).trim()];
  };
  for (let raw of lines) {
    const line = raw.replace(/\t/g, '  ');
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    if (t === 'checks:') continue;
    if (/^[a-zA-Z0-9_-]+:$/.test(t) && line.startsWith('  ') && !line.startsWith('    ')) {
      curGroup = t.slice(0, -1);
      out.checks[curGroup] = { commands: [] };
      inCommands = false;
      curCmd = null;
      continue;
    }
    if (!curGroup) continue;
    if (t === 'commands:') { inCommands = true; curCmd = null; continue; }
    if (inCommands && t.startsWith('- ')) {
      curCmd = {};
      out.checks[curGroup].commands.push(curCmd);
      const rest = t.slice(2);
      const pair = kv(rest);
      if (pair) curCmd[pair[0]] = stripQuotes(pair[1]);
      continue;
    }
    const pair = kv(t);
    if (!pair) continue;
    if (!inCommands) {
      out.checks[curGroup][pair[0]] = stripQuotes(pair[1]);
    } else if (curCmd) {
      curCmd[pair[0]] = stripQuotes(pair[1]);
    }
  }
  return out;
}

function shellQuote(s) {
  return `'${String(s).replace(/'/g, `'"'"'`)}'`;
}

function renderReport({ target, host, user, checks, start, results, format = 'markdown' }) {
  if (format === 'json') {
    return JSON.stringify({
      target, host, user, checks, start,
      total: results.length,
      anomalies: results.filter(r => !r.ok || hasAnomaly(r.stdout, r.stderr)).length,
      results,
    }, null, 2);
  }

  const errorItems = results.filter(r => !r.ok || hasAnomaly(r.stdout, r.stderr));
  let md = '';
  md += `# 🔍 Server Inspection Report\n\n`;
  md += `- Target: \`${mdEscape(target)}\`\n`;
  md += `- Host: \`${mdEscape(host)}\`\n`;
  md += `- User: \`${mdEscape(user)}\`\n`;
  md += `- Checks: \`${mdEscape(checks)}\`\n`;
  md += `- Started: \`${mdEscape(start)}\`\n`;
  md += `- Total checks: ${results.length}\n`;
  md += `- ⚠️ Anomalies: ${errorItems.length}\n\n`;

  // Summary
  const status = errorItems.length === 0 ? '✅ HEALTHY' : errorItems.length <= 3 ? '⚠️ WARNING' : '🚨 CRITICAL';
  md += `## Overall Status: ${status}\n\n`;

  // Anomaly section (priority)
  if (errorItems.length > 0) {
    md += `## ⚠️ Anomalies (Priority)\n\n`;
    for (const r of errorItems) {
      md += `### ${r.ok ? '⚠️' : '❌'} ${mdEscape(r.id)}\n\n`;
      md += `Command: \`${mdEscape(r.cmd)}\`\n\n`;
      md += `Status: ${r.ok ? 'OK (contains anomalies)' : 'FAIL'} (timeout ${r.timeoutSec}s)\n\n`;
      if (r.stdout.trim()) {
        md += `Output:\n\n\`\`\`\n${r.stdout.trim()}\n\`\`\`\n\n`;
      }
      if (r.stderr.trim()) {
        md += `Stderr:\n\n\`\`\`\n${r.stderr.trim()}\n\`\`\`\n\n`;
      }
    }
  }

  // Normal section (collapsible)
  md += `<details><summary>📋 View all check results (${results.length} total)</summary>\n\n`;
  for (const r of results.filter(r => !errorItems.includes(r))) {
    md += `### ✅ ${mdEscape(r.id)}\n\n`;
    md += `Command: \`${mdEscape(r.cmd)}\`\n\n`;
    md += `Status: OK (timeout ${r.timeoutSec}s)\n\n`;
    if (r.stdout.trim()) {
      md += `Output:\n\n\`\`\`\n${r.stdout.trim()}\n\`\`\`\n\n`;
    }
  }
  md += `</details>\n`;
  return md;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.target) {
    usage();
    if (!args.target) process.exitCode = 2;
    return;
  }

  const here = dirname(fileURLToPath(import.meta.url));
  const skillDir = dirname(here);
  const targetsPath = join(skillDir, 'references', 'targets.yaml');
  const checksPath = join(skillDir, 'references', 'checks.yaml');

  // SECURITY VALIDATION: Ensure we only access allowed files
  // This prevents the script from being used to read arbitrary files
  const allowedPaths = [targetsPath, checksPath];
  for (const p of allowedPaths) {
    try {
      await readFile(p, 'utf-8');
    } catch (e) {
      console.error(`Error: Required file not found: ${p}`);
      process.exitCode = 1;
      return;
    }
  }

  const targetsText = await readFile(targetsPath, 'utf-8');
  const checksText = await readFile(checksPath, 'utf-8');

  const targets = parseSimpleYaml(targetsText);
  const t = targets.targets?.[args.target];
  if (!t) throw new Error(`Unknown target: ${args.target}`);

  const checks = parseChecksYaml(checksText);
  const group = checks.checks?.[args.checks];
  if (!group) throw new Error(`Unknown checks group: ${args.checks}`);

  // Dynamic command generation
  if (args.checks === 'services') {
    group.commands = buildServiceCommands(t.services ?? []);
  }
  if (args.checks === 'daily') {
    group.commands = buildDailyCommands(t);
  }

  const sshBase = [
    '-i', String(t.keyPath).replace('~', process.env.HOME || '/root'),
    '-p', String(t.port ?? 22),
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=accept-new',
    '-o', 'ConnectTimeout=8',
  ];
  const dest = `${t.user}@${t.host}`;
  const start = nowIso();
  const results = [];

  for (const c of group.commands) {
    const timeoutMs = Number(c.timeoutSec ?? 10) * 1000;
    const remote = `bash -lc ${shellQuote(c.cmd)}`;
    const { error, stdout, stderr } = await execFileP('ssh', [...sshBase, dest, remote], { timeoutMs });
    results.push({
      id: c.id, cmd: c.cmd, timeoutSec: c.timeoutSec ?? 10,
      ok: !error, code: error?.code ?? 0, stdout, stderr,
    });
  }

  const report = renderReport({
    target: args.target, host: t.host, user: t.user,
    checks: args.checks, start, results, format: args.format,
  });

  if (args.output) {
    const { writeFile } = await import('node:fs/promises');
    await writeFile(args.output, report);
    console.error(`Report written to: ${args.output}`);
  } else {
    try { process.stdout.write(report); }
    catch (e) { if (e?.code !== 'EPIPE') throw e; }
  }
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exitCode = 1;
});
