---
name: runbook-generator
description: Generate operational runbooks from project files. Scans Dockerfiles, docker-compose.yml, systemd units, Makefiles, package.json, and config files to produce step-by-step operational runbooks with start/stop/restart/deploy/rollback/troubleshoot procedures. Use when asked to create a runbook, generate ops docs, create operational documentation, build a deployment guide, document service procedures, or create an SRE runbook. Triggers on "create runbook", "ops documentation", "deployment guide", "operational docs", "SRE runbook", "service procedures", "how to deploy".
---

# Runbook Generator

Generate operational runbooks by scanning project infrastructure files. Produces structured Markdown runbooks with procedures for common ops tasks.

## Quick Generate

```bash
python3 scripts/generate_runbook.py /path/to/project
```

## Output Formats

```bash
# Markdown (default)
python3 scripts/generate_runbook.py /path/to/project

# JSON (structured)
python3 scripts/generate_runbook.py /path/to/project --format json

# Specific output file
python3 scripts/generate_runbook.py /path/to/project -o RUNBOOK.md
```

## What It Scans

| File | What It Extracts |
|------|-----------------|
| Dockerfile | Base image, exposed ports, entrypoint, build steps |
| docker-compose.yml | Services, ports, volumes, dependencies, env vars |
| systemd units (.service) | ExecStart/Stop/Reload, dependencies, restart policy |
| Makefile | Targets (build, test, deploy, clean, etc.) |
| package.json | Scripts (start, build, test, dev, deploy) |
| .env / .env.example | Required environment variables |
| nginx.conf | Upstream servers, listen ports, locations |

## Generated Sections

1. **Overview** — Service name, description, tech stack
2. **Prerequisites** — Required tools, access, credentials
3. **Environment Variables** — Required vars with descriptions
4. **Build** — How to build the project
5. **Deploy** — Step-by-step deployment procedure
6. **Start/Stop/Restart** — Service lifecycle commands
7. **Health Check** — How to verify the service is running
8. **Rollback** — How to revert to previous version
9. **Troubleshooting** — Common issues and solutions
10. **Monitoring** — Logs, metrics, alerts
11. **Contacts** — On-call, escalation (template)

## Workflow

1. User points to a project directory
2. Script scans for infrastructure files
3. Extracts operational information
4. Generates structured runbook
5. Present to user for review and customization
