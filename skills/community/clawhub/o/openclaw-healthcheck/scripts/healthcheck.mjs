#!/usr/bin/env node
import { execSync } from 'child_process';
import fs from 'fs';
import os from 'os';

function run(cmd) {
  try {
    return { ok: true, out: execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim() };
  } catch (e) {
    return { ok: false, out: (e.stdout || e.stderr || e.message || '').toString().trim() };
  }
}

const findings = [];
const recommendations = [];
const evidence = {};
let score = 100;

const status = run('openclaw status');
evidence.openclawStatus = status.out.slice(0, 4000);
if (!status.ok) {
  findings.push({ level: 'HIGH', area: 'runtime', issue: 'openclaw status failed' });
  recommendations.push('Run `openclaw status` manually and fix gateway/runtime health before production use.');
  score -= 35;
}

const ports = run("lsof -nP -iTCP -sTCP:LISTEN | egrep '18789|3000|9222|chrome|node|electron' || true");
evidence.listeners = ports.out;
if (/9222/.test(ports.out)) {
  findings.push({ level: 'MEDIUM', area: 'browser', issue: 'Chrome remote debugging listener detected (9222)' });
  recommendations.push('Verify Chrome existing-session / remote debugging is enabled intentionally and not left open unnecessarily.');
  score -= 10;
}
if (/18789/.test(ports.out) === false) {
  findings.push({ level: 'MEDIUM', area: 'gateway', issue: 'Expected gateway listener 18789 not visible' });
  recommendations.push('Verify gateway is running and listening on the expected port/interface.');
  score -= 10;
}

const configPath = os.homedir() + '/.openclaw/openclaw.json';
if (fs.existsSync(configPath)) {
  const raw = fs.readFileSync(configPath, 'utf8');
  evidence.configPath = configPath;
  try {
    const cfg = JSON.parse(raw);
    const acpx = cfg?.plugins?.entries?.acpx?.config;
    if (acpx?.permissionMode === 'approve-all') {
      findings.push({ level: 'MEDIUM', area: 'config', issue: 'acpx permissionMode is approve-all' });
      recommendations.push('Review whether `approve-all` is still necessary; prefer narrower modes where practical.');
      score -= 8;
    }
    if (JSON.stringify(cfg).includes('chrome-relay')) {
      findings.push({ level: 'LOW', area: 'browser', issue: 'chrome-relay/browser attach capabilities present' });
      recommendations.push('Ensure browser relay / existing-session access is intentional and user-approved.');
      score -= 3;
    }
  } catch {
    findings.push({ level: 'MEDIUM', area: 'config', issue: 'openclaw.json is not valid JSON' });
    recommendations.push('Repair invalid openclaw.json before relying on this deployment.');
    score -= 20;
  }
} else {
  findings.push({ level: 'LOW', area: 'config', issue: 'openclaw.json not found at default path' });
  score -= 3;
}

const recentLog = run("tail -n 200 /tmp/openclaw/openclaw-$(date +%F).log 2>/dev/null || true");
evidence.recentLog = recentLog.out.slice(0, 4000);
if (/AcpRuntimeError|Permission denied|exited with code 1|prerender-error|Could not find LinkedIn editor/i.test(recentLog.out)) {
  findings.push({ level: 'MEDIUM', area: 'logs', issue: 'Recent runtime errors detected in gateway log' });
  recommendations.push('Review recent log errors and clear repeated operational failures before wider rollout.');
  score -= 10;
}

let verdict = 'PASS';
if (score < 60 || findings.some(f => f.level === 'HIGH')) verdict = 'FAIL';
else if (score < 85 || findings.some(f => f.level === 'MEDIUM')) verdict = 'WARN';

console.log(JSON.stringify({ score, verdict, findings, recommendations, evidence }, null, 2));
process.exit(verdict === 'FAIL' ? 1 : 0);
