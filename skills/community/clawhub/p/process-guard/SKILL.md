---
name: "ProcessGuard — Critical Process Monitor & Auto-Restart"
description: "Monitor critical processes and auto-restart on failure. Tracks CPU and memory usage, escalates alerts via webhook, callback, or file, and writes a dead man's switch heartbeat so you know if ProcessGuard itself goes down. HTTP dashboard included. Zero required dependencies — CPU/memory monitoring unlocked with optional pidusage install."
author: "@TheShadowRose"
version: "2.1.4"
tags: ["process-guard", "monitor", "auto-restart", "uptime", "devops"]
license: "MIT"
---

# ProcessGuard — Critical Process Monitor & Auto-Restart

Keep services running without babysitting. Define processes, configure health checks, and let ProcessGuard handle the rest.

## What It Does

- **Health checks** — HTTP, TCP port, PID file, or shell command
- **Auto-restart** — configurable retry limits and cooldown delays
- **CPU & memory monitoring** — per-process thresholds with alerts (requires `npm install pidusage`)
- **Alert escalation** — warning → critical, delivered via callback / webhook / JSON file
- **Dead man's switch** — heartbeat file updated every 10s so external monitors know if ProcessGuard itself crashes
- **HTTP dashboard** — optional `/status` endpoint for real-time JSON status
- **Command allowlist** — optionally restrict which executables restart/check commands may use

## Quick Setup

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
  dashboardPort: 9090,
  alert: {
    onAlert: async (alert) => console.error(`ALERT: ${alert.message}`)
  }
});

guard.start();
```

See README.md for full documentation, all config options, and advanced examples.


