/**
 * ProcessGuard v2.1.4 - Critical Process Monitor & Auto-Restart
 * Full feature: CPU/memory monitoring, alert escalation, dead man's switch, dashboard
 * @author @TheShadowRose
 * @license MIT
 */

'use strict';

const http = require('http');
const https = require('https');
const net = require('net');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');

// Optional dependency - install with: npm install pidusage
// If not installed, CPU/memory monitoring is gracefully skipped
let pidusage = null;
try { pidusage = require('pidusage'); } catch {}

class ProcessGuard {
  constructor(options = {}) {
    this.processes = options.processes || [];
    this.checkInterval = options.checkInterval || 30000;
    this.logFile = options.logFile || './process-guard.log';
    this.heartbeatFile = options.heartbeatFile || './process-guard.heartbeat';
    this.heartbeatInterval = options.heartbeatInterval || 10000;
    this.dashboardPort = options.dashboardPort || null;

    // Security model - one of the two must be set:
    //   commandAllowlist: ['node', 'ollama', 'npm', 'pm2']  - only these executables are permitted (recommended)
    //   allowAnyCommand: true                                 - explicitly opt out of allowlist enforcement
    // Neither set = construction throws. Shell injection operators are always blocked regardless.
    this.commandAllowlist = options.commandAllowlist || null;
    this.allowAnyCommand = options.allowAnyCommand || false;

    // Alert targets - any combination:
    //   onAlert: async (alert) => {}   callback
    //   webhook: 'https://...'          HTTP POST JSON
    //   file: './alerts.jsonl'          append JSON lines
    this.alert = options.alert || {};

    this._timer = null;
    this._heartbeatTimer = null;
    this._httpServer = null;

    this.stats = {};
    for (const p of this.processes) {
      this._initStats(p.name);
    }

    // Validate at construction time - throws synchronously on bad config
    this._validateConfig();
  }

  _initStats(name) {
    this.stats[name] = {
      restarts: 0,
      firstSeen: Date.now(),
      lastUp: Date.now(),
      downtime: 0,
      uptimePercent: 100,
      cpu: null,
      memory: null,
      alertsSent: 0,
      stage: 'ok',          // ok | warning | critical
      restartHistory: []
    };
  }

  // ─── Lifecycle ────────────────────────────────────────────────────────────

  async start() {
    this._log('ProcessGuard v2.0.0 started');
    this._startHeartbeat();
    if (this.dashboardPort) this._startDashboard(this.dashboardPort);
    await this.checkAll();
    this._timer = setInterval(() => this.checkAll(), this.checkInterval);
  }

  stop() {
    if (this._timer) clearInterval(this._timer);
    if (this._heartbeatTimer) clearInterval(this._heartbeatTimer);
    if (this._httpServer) this._httpServer.close();
    // Clean up heartbeat file so external monitors know we stopped intentionally
    try { fs.writeFileSync(this.heartbeatFile, JSON.stringify({ stopped: true, at: new Date().toISOString() })); } catch {}
    this._log('ProcessGuard stopped');
  }

  // ─── Config Validation ────────────────────────────────────────────────────

  _validateConfig() {
    // Require explicit security posture - no silent defaults that execute arbitrary commands
    const hasRestartCommands = this.processes.some(p => p.restart);
    if (hasRestartCommands && !this.commandAllowlist && !this.allowAnyCommand) {
      throw new Error(
        'ProcessGuard requires an explicit security posture for restart commands.\n' +
        '  Option A (recommended): set commandAllowlist: [\'node\', \'pm2\', ...] to restrict allowed executables.\n' +
        '  Option B: set allowAnyCommand: true to permit any executable (not recommended for production).\n' +
        'Shell injection operators (;, &, |, `, $, <, >) are always blocked regardless of setting.'
      );
    }
    for (const p of this.processes) {
      if (!p.name) throw new Error('Each process config must have a name');
      if (p.restart !== undefined && typeof p.restart !== 'string') {
        throw new Error(`restart command for "${p.name}" must be a string`);
      }
      // Shell operator blocking is ALWAYS enforced - independent of allowlist/allowAnyCommand
      this._blockShellOperators(p.name, 'restart', p.restart);
      this._blockShellOperators(p.name, 'check.command', p.check?.command);
      // Allowlist enforcement is additional (when configured)
      if (this.commandAllowlist) {
        this._assertAllowlisted(p.name, 'restart', p.restart);
        this._assertAllowlisted(p.name, 'check.command', p.check?.command);
      }
    }
  }

  _blockShellOperators(name, field, cmd) {
    if (!cmd) return;
    if (/[;&|`$<>\n]/.test(cmd)) {
      throw new Error(
        `${name} ${field} contains shell operators which are not permitted: "${cmd}". ` +
        'Shell injection operators (;, &, |, `, $, <, >) are always blocked regardless of security posture.'
      );
    }
  }

  _assertAllowlisted(name, field, cmd) {
    if (!cmd) return;
    // Shell operators already blocked by _blockShellOperators() before this is called
    const exe = cmd.trim().split(/\s+/)[0];
    if (!this.commandAllowlist.includes(exe)) {
      throw new Error(`${name} ${field} uses "${exe}" which is not in commandAllowlist`);
    }
  }

  _sanitizeCommand(cmd) {
    // Always block shell injection operators - even without an allowlist configured
    if (/[;&|`$<>\n]/.test(cmd)) {
      throw new Error(`Command contains shell operators which are not permitted: "${cmd}". Use simple commands without shell chaining.`);
    }
  }

  // ─── Main Check Loop ──────────────────────────────────────────────────────

  async checkAll() {
    for (const proc of this.processes) {
      if (!this.stats[proc.name]) this._initStats(proc.name);
      const s = this.stats[proc.name];
      const alive = await this._check(proc);

      if (alive) {
        if (s.stage === 'warning' || s.stage === 'critical') {
          this._log(`${proc.name}: RECOVERED`);
          s.stage = 'ok';
        }
        s.lastUp = Date.now();
        await this._updateResourceUsage(proc);
        this._checkResourceThresholds(proc);
      } else {
        s.downtime += this.checkInterval;
        const elapsed = Date.now() - s.firstSeen;
        s.uptimePercent = Math.max(0, 100 - (s.downtime / elapsed) * 100);

        const max = proc.maxRestarts !== undefined ? proc.maxRestarts : 5;
        if (s.restarts < max) {
          this._log(`${proc.name}: DOWN - restart attempt ${s.restarts + 1}/${max}`);
          s.stage = 'warning';
          const ok = await this._restart(proc);
          if (ok) {
            s.restarts++;
            s.restartHistory.push({ at: new Date().toISOString(), attempt: s.restarts });
            if (s.restartHistory.length > 50) s.restartHistory.shift();
          }
        } else if (s.stage !== 'critical') {
          s.stage = 'critical';
          this._log(`${proc.name}: MAX RESTARTS REACHED - manual intervention required`);
          await this._sendAlert({
            level: 'critical',
            process: proc.name,
            message: `${proc.name} is DOWN after ${s.restarts} restart attempts. Manual intervention required.`,
            restarts: s.restarts,
            at: new Date().toISOString()
          });
        }
      }
    }
  }

  // ─── Health Checks ────────────────────────────────────────────────────────

  async _check(proc) {
    const c = proc.check;
    if (!c) return true;
    if (typeof c === 'string') return this._httpCheck(c);
    if (c.port) return this._tcpCheck(c.host || 'localhost', c.port);
    if (c.pid_file) return this._pidCheck(c.pid_file);
    if (c.command) {
      this._blockShellOperators(proc.name, 'check.command', c.command); // runtime guard (belt+suspenders)
      // spawnSync with shell:false — no shell interpolation, no injection surface
      const parts = c.command.trim().split(/\s+/);
      const r = spawnSync(parts[0], parts.slice(1), { timeout: 5000, stdio: 'pipe', shell: false });
      return r.status === 0;
    }
    return true;
  }

  _httpCheck(url) {
    const client = url.startsWith('https') ? https : http;
    return new Promise(resolve => {
      const req = client.get(url, { timeout: 5000 }, res => {
        res.resume(); // drain
        resolve(res.statusCode < 500);
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
    });
  }

  _tcpCheck(host, port) {
    return new Promise(resolve => {
      const sock = new net.Socket();
      sock.setTimeout(3000);
      sock.connect(port, host, () => { sock.destroy(); resolve(true); });
      sock.on('error', () => resolve(false));
      sock.on('timeout', () => { sock.destroy(); resolve(false); });
    });
  }

  _pidCheck(pidFile) {
    try {
      const pid = parseInt(fs.readFileSync(pidFile, 'utf8').trim(), 10);
      if (isNaN(pid)) return false;
      process.kill(pid, 0); // signal 0 = existence check, no actual signal
      return true;
    } catch { return false; }
  }

  // ─── Resource Monitoring ─────────────────────────────────────────────────

  async _updateResourceUsage(proc) {
    if (!pidusage) return; // graceful degradation - install pidusage to enable
    const pid = this._resolvePid(proc);
    if (!pid) return;
    try {
      const usage = await pidusage(pid);
      const s = this.stats[proc.name];
      s.cpu = Math.round(usage.cpu * 10) / 10;       // percent
      s.memory = Math.round(usage.memory / 1024 / 1024 * 10) / 10; // MB
    } catch {}
  }

  _resolvePid(proc) {
    if (proc.pid) return proc.pid;
    if (proc.check?.pid_file) {
      try { return parseInt(fs.readFileSync(proc.check.pid_file, 'utf8').trim(), 10); } catch {}
    }
    return null;
  }

  _checkResourceThresholds(proc) {
    if (!proc.thresholds) return;
    const s = this.stats[proc.name];
    const t = proc.thresholds;

    if (t.maxCpuPercent && s.cpu !== null && s.cpu > t.maxCpuPercent) {
      this._log(`${proc.name}: HIGH CPU ${s.cpu}% (threshold: ${t.maxCpuPercent}%)`);
      if (s.stage === 'ok') {
        s.stage = 'warning';
        this._sendAlert({
          level: 'warning',
          process: proc.name,
          message: `${proc.name} CPU at ${s.cpu}% - threshold is ${t.maxCpuPercent}%`,
          metric: 'cpu',
          value: s.cpu
        });
      }
    }

    if (t.maxMemoryMb && s.memory !== null && s.memory > t.maxMemoryMb) {
      this._log(`${proc.name}: HIGH MEMORY ${s.memory}MB (threshold: ${t.maxMemoryMb}MB)`);
      if (s.stage === 'ok') {
        s.stage = 'warning';
        this._sendAlert({
          level: 'warning',
          process: proc.name,
          message: `${proc.name} memory at ${s.memory}MB - threshold is ${t.maxMemoryMb}MB`,
          metric: 'memory',
          value: s.memory
        });
      }
    }
  }

  // ─── Restart ─────────────────────────────────────────────────────────────

  async _restart(proc) {
    if (!proc.restart) {
      this._log(`${proc.name}: no restart command configured`);
      return false;
    }
    // Always sanitize (blocks shell operators); allowlist check happens in _validateConfig at startup
    this._sanitizeCommand(proc.restart);
    if (proc.cooldown) await new Promise(r => setTimeout(r, proc.cooldown));
    // spawn with shell:false — no shell interpolation, no injection surface
    const parts = proc.restart.trim().split(/\s+/);
    return new Promise(resolve => {
      const child = spawn(parts[0], parts.slice(1), { shell: false, stdio: 'ignore' });
      const killTimer = setTimeout(() => { try { child.kill(); } catch {} resolve(false); }, 15000);
      child.on('error', (err) => {
        clearTimeout(killTimer);
        this._log(`${proc.name}: restart FAILED - ${err.message}`);
        resolve(false);
      });
      child.on('close', (code) => {
        clearTimeout(killTimer);
        this._log(code === 0 ? `${proc.name}: restart OK` : `${proc.name}: restart exited ${code}`);
        resolve(code === 0);
      });
    });
  }

  // ─── Alert Escalation ────────────────────────────────────────────────────

  async _sendAlert(alert) {
    const s = this.stats[alert.process];
    if (s) s.alertsSent++;
    this._log(`ALERT [${alert.level.toUpperCase()}] ${alert.message}`);

    // Callback
    if (typeof this.alert.onAlert === 'function') {
      try { await this.alert.onAlert(alert); } catch (e) {
        this._log(`onAlert callback error: ${e.message}`);
      }
    }

    // Webhook (non-blocking)
    if (this.alert.webhook) this._webhookPost(this.alert.webhook, alert);

    // File (JSON lines)
    if (this.alert.file) {
      try {
        fs.appendFileSync(this.alert.file, JSON.stringify({ ...alert, sentAt: new Date().toISOString() }) + '\n');
      } catch (e) { this._log(`Alert file write error: ${e.message}`); }
    }
  }

  _webhookPost(url, payload) {
    const body = JSON.stringify(payload);
    const client = url.startsWith('https') ? https : http;
    try {
      const u = new URL(url);
      const req = client.request({
        hostname: u.hostname,
        port: u.port || (url.startsWith('https') ? 443 : 80),
        path: u.pathname + (u.search || ''),
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
        timeout: 5000
      }, res => { res.resume(); });
      req.on('error', e => this._log(`Webhook error: ${e.message}`));
      req.write(body);
      req.end();
    } catch (e) { this._log(`Webhook failed: ${e.message}`); }
  }

  // ─── Dead Man's Switch ───────────────────────────────────────────────────

  _startHeartbeat() {
    const write = () => {
      try {
        fs.writeFileSync(this.heartbeatFile, JSON.stringify({
          alive: true,
          pid: process.pid,
          at: Date.now(),
          iso: new Date().toISOString(),
          processCount: this.processes.length
        }));
      } catch {}
    };
    write();
    this._heartbeatTimer = setInterval(write, this.heartbeatInterval);
    this._log(`Dead man's switch: writing heartbeat to ${this.heartbeatFile} every ${this.heartbeatInterval / 1000}s`);
  }

  // ─── HTTP Dashboard ──────────────────────────────────────────────────────

  _startDashboard(port) {
    this._httpServer = http.createServer((req, res) => {
      if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        return res.end('OK');
      }
      if (req.url === '/status' || req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify(this.status(), null, 2));
      }
      res.writeHead(404);
      res.end('Not found');
    });
    this._httpServer.listen(port, () => {
      this._log(`Dashboard: http://localhost:${port}/status`);
    });
  }

  // ─── Status ──────────────────────────────────────────────────────────────

  status() {
    return this.processes.map(p => {
      const s = this.stats[p.name];
      return {
        name: p.name,
        stage: s.stage,
        icon: { ok: '✅', warning: '⚠️', critical: '🔴' }[s.stage] || '❓',
        uptimePercent: Math.round(s.uptimePercent * 10) / 10,
        restarts: s.restarts,
        lastUp: new Date(s.lastUp).toISOString(),
        cpu: s.cpu !== null ? `${s.cpu}%` : 'n/a (install pidusage)',
        memory: s.memory !== null ? `${s.memory}MB` : 'n/a (install pidusage)',
        alertsSent: s.alertsSent,
        recentRestarts: s.restartHistory.slice(-5)
      };
    });
  }

  printDashboard() {
    const rows = this.status();
    const bar = '─'.repeat(64);
    console.log(`\n🛡️  ProcessGuard Status - ${new Date().toLocaleTimeString()}`);
    console.log(bar);
    for (const r of rows) {
      const name = r.name.padEnd(18);
      const up = `${r.uptimePercent}%`.padStart(7);
      const cpu = r.cpu.padStart(12);
      const mem = r.memory.padStart(10);
      const restarts = `${r.restarts} restart${r.restarts !== 1 ? 's' : ''}`;
      console.log(`${r.icon} ${name} ${up} uptime | CPU:${cpu} | Mem:${mem} | ${restarts}`);
    }
    console.log(bar + '\n');
  }

  // ─── Logging ─────────────────────────────────────────────────────────────

  _log(msg) {
    const line = `[${new Date().toISOString()}] ${msg}`;
    console.log(line);
    try { fs.appendFileSync(this.logFile, line + '\n'); } catch {}
  }
}

module.exports = { ProcessGuard };


