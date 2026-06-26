---
name: docker-health-monitor
description: 'Monitor Docker container health: running status, CPU/memory usage, restart counts, and available image updates. Use when a user requests Docker health checks, container monitoring, resource usage reports, restart tracking, or image freshness audits — run targeted checks or a full health report.'
---

# Docker Health Monitor

## Script

`scripts/docker-health.sh` — the single entry point for all checks.

The script is self-contained and works on any system with Docker installed. It auto-detects the Docker socket availability and gracefully handles permission issues.

## Quick Start

Run a full health report:

```bash
bash scripts/docker-health.sh --all
```

Or with no arguments (same as `--all`):

```bash
bash scripts/docker-health.sh
```

## Individual Checks

Run any single check by name:

| Command | What it checks |
|---|---|
| `--status` | Lists all containers with their current status (running, stopped, paused, etc.) |
| `--resources` | Shows CPU and memory usage per container via `docker stats` |
| `--restarts` | Flags containers that have restarted more than 3 times |
| `--images` | Checks for available image updates by comparing local image digests with registry |
| `--full` | Runs all checks in sequence (same as `--all`) |

Example:

```bash
bash scripts/docker-health.sh --status --restarts
```

## Full Audit Workflow

1. Run `bash scripts/docker-health.sh --all`
2. The script outputs a formatted report to stdout
3. Key sections: container status summary, resource usage table, restart warnings, image update availability

## Common Findings & Recommendations

- **High restart counts** (>3): Indicates container instability — check logs with `docker logs <container>` and review healthcheck configuration
- **High memory usage**: Consider setting `--memory` limits in the container's run/stack config; check for memory leaks in the application
- **High CPU usage**: Investigate application processes; consider CPU limits or horizontal scaling
- **Outdated images**: Run `docker pull` to update images; consider automated update workflows (watchtower, renovate-bot)
- **Exited containers**: Check exit codes — 0 means intentional stop, non-zero indicates errors

## Notes

- Requires access to the Docker socket (`/var/run/docker.sock`) — run as root or add user to the `docker` group
- `--resources` runs `docker stats` in non-streaming mode (one-shot per container) for quick snapshots
- `--images` checks are advisory — uses `docker inspect` for image digests and checks for newer versions; requires network access to the registry
- Works with both local Docker and remote Docker contexts (DOCKER_HOST env var)
