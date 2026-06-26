---
name: ops-deck
version: 1.0.0
description: "Full operational dashboard for AI agent setups. Cron job calendar, agent intel feeds, security audit panel, network infrastructure map, code search, repo architecture viewer, prompt library, and sprint backlog tracker. Built for indie devs, small teams, and CS students running OpenClaw or similar agent stacks."
tags:
  - dashboard
  - devops
  - monitoring
  - security
  - infrastructure
  - agent-tools
  - cron
  - code-search
  - prompt-library
  - intel
category: tools
---

# Ops Deck — Full Operational Dashboard

A self-hosted operational dashboard for developers running AI agent stacks. See everything in one place: cron jobs, agent intel, security posture, infrastructure map, code search, and more.

For a simpler setup with just code search and prompt library, see [ops-deck-lite](https://clawhub.com/solomonneas/ops-deck-lite).

## What You Get

### Core Modules

| Module | Port | Description |
|--------|------|-------------|
| **Ops Deck UI** | 5173 | Vite + React dashboard (all modules in one UI) |
| **Ops Deck API** | 8005 | Express backend serving all data endpoints |
| **Code Search** | 5204 | Semantic code search with local embeddings |
| **Prompt Library** | 5202 | Categorized, searchable prompt templates |

### Dashboard Panels

**1. Memory Browser**
Searchable knowledge card viewer. Browse cards by category and tags, read full content with rendered markdown. Cards use YAML frontmatter for metadata (topic, category, tags, dates).

**2. Journal**
Date-based daily log viewer. See which days have entries, click to read. Great for tracking what your agent did each day.

**3. Workspace Config**
Tabbed viewer for your agent configuration files: AGENTS.md, SOUL.md, TOOLS.md, USER.md, MEMORY.md, IDENTITY.md. See your full agent personality and config at a glance.

**4. Cron Job Calendar**
Visual calendar of all scheduled agent tasks. See what runs when, last status, next run, error streaks. Click to view payload and delivery config.

```bash
# The API reads from a cron-jobs.json file, updated by a nightly cron
GET /api/cron-jobs
```

**2. Agent Intel Feed**
Aggregated intelligence from automated research crons. Three categories:
- **Cyber Threats:** CVEs, active exploits, advisories (from CISA, BleepingComputer, etc.)
- **AI Lab Updates:** Model releases, API changes, pricing updates
- **Dev Tooling:** Framework updates, SDK releases, breaking changes

```bash
# Intel entries with category filtering
GET /api/agent-intel
GET /api/agent-intel?category=model-updates
POST /api/agents/intel   # Add new intel entry
```

**3. Security Audit Panel**
Live security posture dashboard. Tracks firewall rules, fail2ban status, SSH config, listening ports, AppArmor status, and pending security updates.

```bash
# Security audit data (updated by a daily cron)
GET /api/security-audit
```

Data structure:
```json
{
  "lastUpdated": "2026-03-21T04:00:00Z",
  "securityControls": [
    {"name": "UFW Firewall", "status": "active", "lastChecked": "2026-03-21"},
    {"name": "Fail2ban", "status": "active", "bannedIPs": 42},
    {"name": "SSH Config", "status": "hardened", "passwordAuth": false}
  ],
  "auditLog": []
}
```

**4. Network Infrastructure Map**
Visual map of your services, ports, and connections. Populated from a JSON config file you maintain manually or generate with your own scripts.

```bash
# Architecture/infrastructure data
GET /api/architecture
```

**5. Code Search** (same as ops-deck-lite)
Semantic search across your entire codebase using local embeddings.

```bash
POST http://localhost:5204/api/search
{"query": "authentication middleware", "mode": "hybrid", "limit": 10}
```

**6. Prompt Library** (same as ops-deck-lite)
Categorized prompt templates. Stop rewriting the same prompts.

```bash
GET /api/prompts         # List all
POST /api/prompts        # Create new
```

**7. Sprint Backlog Tracker**
Kanban-style task tracking synced with your git repos. Auto-detects progress from recent commits.

```bash
# Backlog data (JSON file, updated by daily cron)
GET /api/backlog
```

## How Data Collection Works

> **The dashboard itself has no system access.** It reads static JSON files that YOU generate separately. The security audit panel, cron calendar, and infrastructure map all display data from JSON files on disk. You control what data goes into those files and how it's collected.
>
> **Example:** The security audit panel reads `security-audit.json`. You can populate this manually, via a cron script you write and review, or skip it entirely. The dashboard never runs `ufw status`, `ss -tlnp`, or any system command on its own.
>
> **No elevated privileges required.** The dashboard services run as a normal user. If you want automated data collection, the setup guide includes example cron scripts that you review and configure yourself.

## Architecture

```
┌──────────────────────────────────────┐
│           Ops Deck UI (:5173)        │
│  React + Vite + Tailwind             │
│  Panels: Cron | Intel | Security |   │
│  Infra | Code | Prompts | Backlog    │
└──────────┬───────────────────────────┘
           │
     ┌─────┴─────┐
     │            │
┌────▼────┐  ┌───▼────────┐
│ API     │  │ Code Search │
│ (:8005) │  │ (:5204)     │
│ Express │  │ FastAPI     │
└────┬────┘  └─────────────┘
     │
┌────▼──────────┐
│ Prompt Library │
│ (:5202)        │
│ Express        │
└────────────────┘
```

All services are local only. No cloud dependencies. No telemetry.

## Prerequisites

- Node.js 18+
- Python 3.10+ with FastAPI
- Ollama with `qwen3-embedding:8b` (for code search embeddings)
- PM2 (process manager)
- SQLite (no external database needed)

## Setup

### 1. Install dependencies

```bash
npm install -g pm2
pip install fastapi uvicorn aiofiles
ollama pull qwen3-embedding:8b
```

### 2. Create the API server

The Ops Deck API is a lightweight Express server that serves JSON data files and provides CRUD endpoints for intel entries.

```bash
mkdir -p ops-deck-api
cd ops-deck-api
npm init -y
npm install express cors
```

Key endpoints to implement:

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const app = express();

app.use(cors());
app.use(express.json());

// Cron jobs (read from file, updated by nightly cron)
app.get('/api/cron-jobs', (req, res) => {
  const data = JSON.parse(fs.readFileSync('./cron-jobs.json', 'utf8'));
  res.json(data);
});

// Agent intel (CRUD)
app.get('/api/agent-intel', (req, res) => { /* ... */ });
app.post('/api/agents/intel', (req, res) => { /* ... */ });

// Security audit (read from file, updated by daily cron)
app.get('/api/security-audit', (req, res) => {
  const data = JSON.parse(fs.readFileSync('./security-audit/audit-data.json', 'utf8'));
  res.json(data);
});

// Architecture
app.get('/api/architecture', (req, res) => { /* ... */ });

// Backlog
app.get('/api/backlog', (req, res) => {
  const data = JSON.parse(fs.readFileSync('./backlog.json', 'utf8'));
  res.json(data);
});

app.listen(8005, () => console.log('Ops Deck API on :8005'));
```

### 3. Create the frontend

```bash
npm create vite@latest ops-deck -- --template react-ts
cd ops-deck
npm install
npm install tailwindcss @headlessui/react recharts
```

Build dashboard panels that fetch from the API endpoints. Each panel is a React component:
- `CronCalendar.tsx` - Monthly calendar view of cron jobs
- `IntelFeed.tsx` - Filterable intel card feed
- `SecurityAudit.tsx` - Status cards for each security control
- `InfraMap.tsx` - Service topology visualization
- `CodeSearch.tsx` - Search input with results display
- `PromptLibrary.tsx` - CRUD interface for prompts
- `Backlog.tsx` - Kanban board from backlog.json

### 4. (Optional) Set up data refresh scripts

The dashboard reads static JSON files. You can update them manually or write your own scripts to automate it. Example scripts are provided in the repo's `docs/` directory for reference. Review them before running.

All data collection is opt-in. The dashboard works with the included example data out of the box.

### 5. PM2 ecosystem config

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [
    {
      name: 'opsdeck',
      cwd: './ops-deck',
      script: 'node_modules/.bin/vite',
      args: '--host --port 5173',
      autorestart: true,
    },
    {
      name: 'opsdeck-api',
      cwd: './ops-deck-api',
      script: 'server.js',
      autorestart: true,
    },
    {
      name: 'code-search',
      cwd: './code-search',
      script: 'server.py',
      interpreter: 'python3',
      autorestart: true,
    },
    {
      name: 'prompt-library-api',
      cwd: './prompt-library/backend',
      script: 'server.js',
      autorestart: true,
    },
  ]
};
```

```bash
pm2 start ecosystem.config.cjs
pm2 save
pm2 startup  # auto-start on boot
```

## Resource Usage

| Service | RAM | CPU | Disk |
|---------|-----|-----|------|
| Ops Deck UI | ~75MB | <1% idle | ~20MB build |
| Ops Deck API | ~85MB | <1% idle | <5MB data |
| Code Search | ~150MB | <1% idle | ~50MB index |
| Prompt Library | ~50MB | <1% idle | <1MB |
| Ollama (shared) | ~4GB | Spikes during indexing | ~4GB model |

Total: ~360MB for all services (Ollama runs independently).

## Customization

The dashboard is yours to extend. Common additions:
- **Social media pipeline** panel (if you run Postiz/n8n)
- **LLM usage tracking** (token counts, costs, model breakdown)
- **Uptime monitoring** (ping your deployed services)
- **Git activity** (commit heatmap, PR status)

## Who This Is For

- **Indie devs** running OpenClaw with multiple cron jobs and services
- **CS students** building a portfolio of operational tools
- **Small teams** who want visibility into their agent infrastructure
- **Homelab enthusiasts** who want a single pane of glass

If you just want code search and prompts, use [ops-deck-lite](https://clawhub.com/solomonneas/ops-deck-lite) instead. This is the full stack.

## Source

https://github.com/solomonneas/ops-deck-oss
