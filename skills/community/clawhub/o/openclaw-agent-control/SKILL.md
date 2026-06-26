---
name: openclaw-agent-control
description: Deploy and start OpenClaw Agent Control with one command (backend + frontend) using skill-based workflow.
---

# OpenClaw Agent Control Skill

## Purpose
Deploy and run OpenClaw Agent Control quickly for operator usage.

## What this skill does
- Clone or update repository.
- Start backend on `8787`.
- Build and start frontend on `3000`.
- Provide health checks and runtime tips.

## Quick Use
```bash
bash scripts/deploy_project.sh
```

## Optional environment variables
- `REPO_URL` default: `https://github.com/JiangAgentLabs/OpenClaw-Agent-Control.git`
- `PROJECT_DIR` default: `/root/OpenClaw-Agent-Control`
- `MONITOR_PORT` default: `8787`
- `PORT` default: `3000`

## Validation
After deployment:
- Frontend: `http://127.0.0.1:3000`
- Backend: `http://127.0.0.1:8787/api/status`
