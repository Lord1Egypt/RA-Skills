# ProcessGuard v2.1.4 — Critical Process Monitor & Auto-Restart

Monitor critical processes, auto-restart on failure, track CPU/memory, alert humans when things go sideways. Keep your services running without babysitting.

> **Security note:** When restart commands are configured, ProcessGuard requires an explicit security posture. Set `commandAllowlist` (recommended) to restrict which executables may run, or set `allowAnyCommand: true` to explicitly permit any executable. Neither set = throws at construction. Shell injection operators (`;`, `&`, `|`, `` ` ``, `$`, `<`, `>`) are always blocked in all commands regardless of setting.

---

## Quick Start

```javascript
const { ProcessGuard } = require('./src/process-guard');

const guard = new ProcessGuard({
  processes: [
    {
      name: 'ollama',
      check: 'http://localhost:11434/api/tags',
      restart: 'ollama serve',
      maxRestarts: 5,
      cooldown: 5000
    }
  ],
  checkInterval: 30000,
  logFile: './process-guard.log'
});

guard.start();
```

---

## Health Check Types

| Type | Config | Description |
|------|--------|-------------|
| HTTP | `check: 'http://localhost:3000/health'` | GET — passes if status < 500 |
| TCP | `check: { port: 6379 }` | Connect to port — passes if connection succeeds |
| PID file | `check: { pid_file: '/run/app.pid' }` | Check if process with that PID is alive |
| Command | `check: { command: 'pgrep myapp' }` | Run command — passes if exit code is 0 |

---

## CPU & Memory Monitoring

Install the optional dependency to enable resource monitoring:

```bash
npm install pidusage
```

Then configure thresholds per process:

```javascript
{
  name: 'my-bot',
  check: { pid_file: '/run/my-bot.pid' },
  restart: 'node bot.js',
  thresholds: {
    maxCpuPercent: 80,     // alert if CPU > 80% sustained
    maxMemoryMb: 512       // alert if memory > 512MB
  }
}
```

If `pidusage` is not installed, resource monitoring is skipped silently — everything else still works.

To give ProcessGuard the PID directly (no pid file needed):

```javascript
{
  name: 'my-service',
  pid: 12345,
  thresholds: { maxCpuPercent: 90 }
}
```

---

## Alert Escalation

Three escalation targets — use any combination:

### Callback

```javascript
const guard = new ProcessGuard({
  alert: {
    onAlert: async (alert) => {
      // alert.level: 'warning' | 'critical'
      // alert.process: process name
      // alert.message: human-readable description
      // alert.metric: 'cpu' | 'memory' (resource alerts only)
      // alert.value: metric value (resource alerts only)
      console.log(`ALERT: ${alert.message}`);
      // send email, push notification, etc.
    }
  }
});
```

### Webhook (HTTP POST)

```javascript
const guard = new ProcessGuard({
  alert: {
    webhook: 'https://hooks.slack.com/services/...'  // or any HTTP endpoint
  }
});
```

Sends a JSON POST body:
```json
{
  "level": "critical",
  "process": "ollama",
  "message": "ollama is DOWN after 5 restart attempts. Manual intervention required.",
  "restarts": 5,
  "at": "2025-01-01T12:00:00.000Z",
  "sentAt": "2025-01-01T12:00:00.001Z"
}
```

### Alert File (JSON lines)

```javascript
const guard = new ProcessGuard({
  alert: {
    file: './alerts.jsonl'    // appends one JSON object per line
  }
});
```

---

## Dead Man's Switch

ProcessGuard writes a heartbeat file every 10 seconds (configurable). If ProcessGuard itself crashes, the heartbeat goes stale — an external watchdog can detect this.

```javascript
const guard = new ProcessGuard({
  heartbeatFile: './process-guard.heartbeat',  // default
  heartbeatInterval: 10000                     // ms, default 10s
});
```

Heartbeat file contents:
```json
{
  "alive": true,
  "pid": 12345,
  "at": 1704067200000,
  "iso": "2025-01-01T12:00:00.000Z",
  "processCount": 3
}
```

Example external watchdog check (shell):
```bash
# Alert if heartbeat is older than 30 seconds
python3 -c "
import json, time, sys
hb = json.load(open('./process-guard.heartbeat'))
age = time.time() - hb['at'] / 1000
if age > 30: sys.exit(1)
"
```

---

## HTTP Dashboard

Enable a local status endpoint:

```javascript
const guard = new ProcessGuard({
  dashboardPort: 9090
});
```

- `GET http://localhost:9090/status` — full JSON status
- `GET http://localhost:9090/health` — plain `OK` (for health checks)

---

## Security Model

ProcessGuard executes the restart/check commands you configure via `child_process.exec` and `execSync`. When restart commands are present, you must explicitly declare a security posture — there is no unsafe default.

### Option A — Command Allowlist (Recommended)

Restrict which executables may be used in restart and check commands:

```javascript
const guard = new ProcessGuard({
  commandAllowlist: ['node', 'ollama', 'npm', 'pm2'],
  processes: [
    {
      name: 'my-api',
      restart: 'node server.js'  // ✅ allowed
    },
    {
      name: 'bad-config',
      restart: 'rm -rf /'        // ❌ throws at construction — 'rm' not in allowlist
    }
  ]
});
```

### Option B — Allow Any Command (Explicit Opt-Out)

If you need executables that vary or can't be enumerated upfront, explicitly acknowledge the risk:

```javascript
const guard = new ProcessGuard({
  allowAnyCommand: true,   // ⚠️ any configured executable will run — audit your configs
  processes: [...]
});
```

### Always Enforced (Both Options)

Shell injection operators are blocked unconditionally in ALL commands at construction time AND at runtime — they cannot be bypassed:

```
; & | ` $ < > \n
```

Example: `restart: 'node server.js && rm -rf /'` → **throws at construction**, regardless of `allowAnyCommand`.

Validation runs at construction — misconfigured commands throw before any monitoring begins.

---

## Full Example

```javascript
const { ProcessGuard } = require('./src/process-guard');

const guard = new ProcessGuard({
  checkInterval: 30000,
  logFile: './guard.log',
  heartbeatFile: './guard.heartbeat',
  dashboardPort: 9090,
  commandAllowlist: ['node', 'ollama', 'nginx'],

  alert: {
    onAlert: async (alert) => {
      if (alert.level === 'critical') {
        // send yourself a message
        console.error(`CRITICAL: ${alert.message}`);
      }
    },
    file: './alerts.jsonl'
  },

  processes: [
    {
      name: 'ollama',
      check: 'http://localhost:11434/api/tags',
      restart: 'ollama serve',
      maxRestarts: 5,
      cooldown: 5000
    },
    {
      name: 'my-api',
      check: { port: 3000 },
      restart: 'node server.js',
      maxRestarts: 3,
      cooldown: 10000,
      thresholds: {
        maxCpuPercent: 85,
        maxMemoryMb: 256
      }
    },
    {
      name: 'nginx',
      check: { command: 'nginx -t' },
      restart: 'nginx',
      maxRestarts: 2
    }
  ]
});

guard.start();

// Print dashboard to console every 60s
setInterval(() => guard.printDashboard(), 60000);
```

---

## Dashboard Output

```
🛡️  ProcessGuard Status — 12:00:00 PM
────────────────────────────────────────────────────────────────
✅ ollama              100.0% uptime | CPU:      1.2% | Mem:   340.5MB | 0 restarts
⚠️  my-api             99.7% uptime | CPU:     87.3% | Mem:   198.2MB | 2 restarts
✅ nginx               100.0% uptime | CPU:       n/a | Mem:       n/a | 0 restarts
────────────────────────────────────────────────────────────────
```

---

## Configuration Reference

### ProcessGuard Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `processes` | Array | `[]` | Process configs to monitor |
| `checkInterval` | number | `30000` | How often to check (ms) |
| `logFile` | string | `./process-guard.log` | Log output path |
| `heartbeatFile` | string | `./process-guard.heartbeat` | Dead man's switch file |
| `heartbeatInterval` | number | `10000` | Heartbeat write interval (ms) |
| `dashboardPort` | number | `null` | Enable HTTP dashboard on this port |
| `commandAllowlist` | string[] | — | **Required** (or `allowAnyCommand`) when restart commands are configured. Restricts restart/check executables to listed names. |
| `allowAnyCommand` | boolean | `false` | Explicit opt-out of allowlist enforcement. Any configured executable will run. Shell operators still always blocked. |
| `alert.onAlert` | function | — | Async callback on any alert |
| `alert.webhook` | string | — | URL to POST alerts to |
| `alert.file` | string | — | Path to append alert JSON lines |

### Per-Process Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | **required** | Unique process identifier |
| `check` | string/object | — | Health check config |
| `restart` | string | — | Shell command to restart the process |
| `maxRestarts` | number | `5` | Max auto-restart attempts before critical alert |
| `cooldown` | number | — | Delay before restart attempt (ms) |
| `pid` | number | — | PID for resource monitoring |
| `thresholds.maxCpuPercent` | number | — | CPU % alert threshold |
| `thresholds.maxMemoryMb` | number | — | Memory MB alert threshold |

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from
  the use or misuse of this software — including but not limited to financial loss,
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read
this disclaimer and agree to use the software entirely at your own risk.

**DATA DISCLAIMER:** This software processes and stores data locally on your system.
The author(s) are not responsible for data loss, corruption, or unauthorized access
resulting from software bugs, system failures, or user error. Always maintain
independent backups of important data. This software does not transmit data externally
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw)*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $30. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)


