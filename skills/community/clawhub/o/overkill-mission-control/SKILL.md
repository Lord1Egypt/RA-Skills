---
name: overkill-mission-control
description: Comprehensive Mission Control dashboard for OpenClaw - monitor agents, automation, teams, documents, messages, and system metrics. Features real-time dashboards, agent-to-agent messaging, task execution, and enterprise-level monitoring.
homepage: https://github.com/your-repo/overkill-mission-control
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "ports": [3000], "services": ["openclaw-gateway"] },
        "install":
          [
            {
              "id": "npm-install",
              "kind": "npm",
              "package": "next",
              "label": "Install Next.js dependencies",
              "command": "npm install",
              "workdir": "mission-control"
            },
            {
              "id": "service",
              "kind": "systemd",
              "label": "Create Mission Control systemd service",
              "path": "/etc/systemd/system/mission-control.service"
            },
            {
              "id": "tailscale",
              "kind": "systemd",
              "label": "Create Tailscale proxy service",
              "path": "/etc/systemd/system/tailscale-serve.service"
            }
          ],
      },
  }
---

# Overkill Mission Control

Enterprise-grade operations dashboard for OpenClaw autonomous agents.

## Overview

Mission Control provides comprehensive monitoring and control for OpenClaw agents, including:
- Real-time dashboard with live metrics
- Agent-to-agent messaging with LLM-powered responses
- Task execution framework
- Automation workflows
- Document management
- Team coordination
- System alerts and SLO tracking

## Quick Start

1. **Start the dashboard:**
   ```bash
   cd ~/.openclaw/workspace-mission-control
   npm run dev
   ```

2. **Access locally:** http://localhost:3000

3. **Access via Tailscale:** https://<your-host>.taila0448b.ts.net (run `tailscale serve 3000` to enable)

## Pages

| Page | Description |
|------|-------------|
| `/` | Main dashboard with live metrics |
| `/tasks` | Task queue and management |
| `/workshop` | Agent workshop with Kanban |
| `/teams` | Team management |
| `/messages` | Agent-to-agent messaging |
| `/documents` | Document storage and management |
| `/automation` | Automation workflows |
| `/intelligence` | System intelligence |
| `/alerts` | Alert management |
| `/slo` | SLO/Error budget tracking |
| `/runbooks` | Runbook automation |
| `/feature-flags` | Feature flag management |
| `/environments` | Environment comparison |
| `/webhooks` | Webhook management |
| `/stats` | Statistics and analytics |
| `/settings` | System settings |

## Features

### Real-time Dashboard
- Live session count
- Active agents
- Resource utilization (CPU, memory, disk)
- System health score
- Task distribution
- Timeline of activities

### Agent-to-Agent Messaging
- Send messages between agents
- LLM-powered responses (MiniMax M2.5)
- Task execution framework
- Auto-acknowledge and respond
- Polling every 60 seconds

### Task Execution
Agents can execute tasks based on message content:
- `researcher`: research, web_search, summarize
- `seo`: keyword_research, audit, analyze_competitors
- `contentwriter`: write_article, rewrite
- `data-analyst`: analyze_data, generate_report
- `designer`: generate_image, create_mockup
- `orchestrator`: delegate, coordinate

### Documents
- Upload PDFs, images, files
- SQLite-backed with FTS5 search
- Collections and tags
- Version history
- Access control (private/agent/team/public)

### Automation
- Visual workflow builder
- Triggers: schedule, webhook, event, manual, condition
- Actions: message, HTTP, task, notify, condition
- Analytics dashboard

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/status` | System status and metrics |
| `/api/mission-control/agents` | List all agents |
| `/api/mission-control/sessions` | Session data |
| `/api/messages` | Agent messaging |
| `/api/messages/polling` | Message polling & execution |
| `/api/documents` | Document management |
| `/api/automation` | Automation workflows |
| `/api/alerts` | Alert management |
| `/api/slo` | SLO tracking |
| `/api/runbooks` | Runbook management |

## Configuration

### Systemd Services

**mission-control.service:**
```ini
[Unit]
Description=Mission Control Dashboard
After=network.target

[Service]
Type=simple
User=broedkrummen
WorkingDirectory=/home/broedkrummen/.openclaw/workspace-mission-control
ExecStart=/usr/bin/npm run dev
Restart=always

[Install]
WantedBy=multi-user.target
```

**tailscale-serve.service:**
```ini
[Unit]
Description=Tailscale Serve for Mission Control
After=network.target tailscaled.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/sudo /usr/bin/tailscale serve 3000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Database

- **Messages:** `/mnt/openclaw/state/messages.db`
- **Documents:** `/mnt/openclaw/state/documents.db`
- **State:** `/mnt/openclaw/state/`

## Environment

- Node.js 22+
- Next.js 16
- SQLite (better-sqlite3)
- Tailwind CSS

## Troubleshooting

### Dashboard not loading
```bash
# Check if server is running
curl http://localhost:3000

# Restart server
sudo systemctl restart mission-control
```

### Tailscale not working
```bash
# Check Tailscale status
tailscale status

# Restart Tailscale serve
sudo systemctl restart tailscale-serve
```

### Messages not being processed
```bash
# Check cron job
cron list

# Manually trigger polling
curl -s http://localhost:3000/api/messages/polling?action=check-all
curl -s -X POST http://localhost:3000/api/messages/polling -H 'Content-Type: application/json' -d '{"action":"execute"}'
```

## Files Structure

```
mission-control/
├── src/
│   ├── app/           # Next.js pages
│   ├── components/    # React components
│   ├── lib/          # Utilities and APIs
│   └── hooks/        # Custom React hooks
├── public/            # Static assets
├── package.json
└── next.config.js
```

## Credits

Built with Next.js, Tailwind CSS, and SQLite.
