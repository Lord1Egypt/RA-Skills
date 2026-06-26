#!/usr/bin/env node
// OpenClaw Recovery Manager — detect-restart-command.mjs
//
// Usage: node detect-restart-command.mjs
//
// Probes the environment to determine the correct restart command for this
// OpenClaw install. Used at setup time so the agent doesn't have to ask the
// user to pick from a list of options they may not understand.
//
// Output format (always stable for agents parsing):
//   DETECTED: <one-line restart command>
//   REASON:   <short human-readable reason>
//   METHOD:   <systemd-user | systemd-system | docker-compose | pid1 | unknown>
//   CONFIDENCE: <high | medium | low>
//
// Exit 0 on successful detection (any confidence). Exit 1 if nothing
// matched — caller should fall back to asking the user.

import { execSync } from 'child_process';
import { existsSync, readFileSync } from 'fs';

function run(cmd) {
  try {
    return execSync(cmd, { stdio: ['ignore', 'pipe', 'ignore'], encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

function report(method, command, reason, confidence) {
  console.log(`DETECTED: ${command}`);
  console.log(`REASON: ${reason}`);
  console.log(`METHOD: ${method}`);
  console.log(`CONFIDENCE: ${confidence}`);
}

// ---- Probe 1: systemd user service ----
const userActive = run('systemctl --user is-active openclaw-gateway 2>/dev/null');
if (userActive === 'active') {
  report(
    'systemd-user',
    'systemctl --user restart openclaw-gateway',
    'systemd user service `openclaw-gateway` is active under --user',
    'high'
  );
  process.exit(0);
}

// ---- Probe 2: systemd system service ----
const systemActive = run('systemctl is-active openclaw-gateway 2>/dev/null');
if (systemActive === 'active') {
  report(
    'systemd-system',
    'sudo systemctl restart openclaw-gateway',
    'system-level systemd service `openclaw-gateway` is active',
    'high'
  );
  process.exit(0);
}

// Also check for common alternative service names
for (const svc of ['openclaw', 'openclaw.service']) {
  const a = run(`systemctl --user is-active ${svc} 2>/dev/null`);
  if (a === 'active') {
    report('systemd-user', `systemctl --user restart ${svc}`,
      `systemd user service \`${svc}\` is active`, 'high');
    process.exit(0);
  }
  const b = run(`systemctl is-active ${svc} 2>/dev/null`);
  if (b === 'active') {
    report('systemd-system', `sudo systemctl restart ${svc}`,
      `system-level systemd service \`${svc}\` is active`, 'high');
    process.exit(0);
  }
}

// ---- Probe 3: Docker Compose ----
function composeServices(cmd) {
  const out = run(`${cmd} 2>/dev/null`);
  if (!out) return [];
  return out.split('\n').map(s => s.trim()).filter(Boolean);
}

let composeCmd = null;
let composeServicesList = composeServices('docker compose ps --services');
if (composeServicesList.length > 0) composeCmd = 'docker compose';
else {
  composeServicesList = composeServices('docker-compose ps --services');
  if (composeServicesList.length > 0) composeCmd = 'docker-compose';
}

if (composeCmd) {
  const match = composeServicesList.find(s => /openclaw|gateway/i.test(s));
  if (match) {
    report(
      'docker-compose',
      `${composeCmd} restart ${match}`,
      `docker-compose service \`${match}\` found via ${composeCmd}`,
      'high'
    );
    process.exit(0);
  }
}

// ---- Probe 4: Running as PID 1 in a container ----
let isContainer = false;
if (existsSync('/.dockerenv')) isContainer = true;
try {
  const cg = readFileSync('/proc/1/cgroup', 'utf8');
  if (/kubepods|containerd|docker/.test(cg)) isContainer = true;
} catch {}

let pid1Cmdline = '';
try {
  pid1Cmdline = readFileSync('/proc/1/cmdline', 'utf8').replace(/\0/g, ' ').trim();
} catch {}

const pid1IsOpenclaw = /openclaw/i.test(pid1Cmdline) ||
  (/\bnode\b/.test(pid1Cmdline) && /openclaw/i.test(pid1Cmdline));

if (isContainer && pid1IsOpenclaw) {
  report(
    'pid1',
    'kill -USR1 1',
    `running in a container with OpenClaw as PID 1 (cmdline: ${pid1Cmdline.slice(0, 120)})`,
    'high'
  );
  process.exit(0);
}

// Non-container but PID 1 is OpenClaw somehow (rare): still correct to USR1
if (pid1IsOpenclaw) {
  report(
    'pid1',
    'kill -USR1 1',
    `PID 1 appears to be OpenClaw (cmdline: ${pid1Cmdline.slice(0, 120)})`,
    'medium'
  );
  process.exit(0);
}

// ---- Probe 5: plain openclaw process (non-managed) ----
// Filter out our own process and anything that just happens to have "openclaw"
// in its path because it's executing out of the skill directory.
const myPid = String(process.pid);
const myPpid = String(process.ppid);
const rawProcs = run('pgrep -af openclaw 2>/dev/null');
const realProcs = rawProcs.split('\n')
  .map(s => s.trim())
  .filter(Boolean)
  .filter(line => {
    const pid = line.split(/\s+/)[0];
    if (pid === myPid || pid === myPpid) return false;
    // Ignore anyone executing this very script
    if (line.includes('detect-restart-command.mjs')) return false;
    // Ignore shells whose arg just happens to contain our script path
    if (/\bpgrep\b/.test(line)) return false;
    return true;
  });

if (realProcs.length > 0) {
  // Found running processes but no managed restart mechanism detected.
  console.log('DETECTED: (none)');
  console.log(`REASON: openclaw process(es) running but no managed restart mechanism detected. pgrep output: ${realProcs.slice(0, 3).join(' | ')}`);
  console.log('METHOD: unknown');
  console.log('CONFIDENCE: low');
  console.log('ACTION: ask the user how they want OpenClaw restarted');
  process.exit(1);
}

// ---- Nothing found ----
console.log('DETECTED: (none)');
console.log('REASON: no systemd service, docker compose service, PID 1 OpenClaw process, or openclaw process found. OpenClaw may not be running, or it is running under a custom supervisor.');
console.log('METHOD: unknown');
console.log('CONFIDENCE: low');
console.log('ACTION: ask the user how they want OpenClaw restarted');
process.exit(1);
