---
name: homelab-runbook
description: Scan and document all running services on this machine — Docker containers, system services (launchd/systemd), and open listening ports. Generates a human-readable Markdown runbook with service names, ports, images, mount points, and health status. Use when the user asks about homelab, runbook, document services, what's running, service inventory, homelab docs, list my services, scan ports, or wants a snapshot of what's active on the host machine. Can run on demand or on a cron schedule. Works on macOS and Linux.
---

# Homelab Runbook

Scan the host machine and generate a Markdown runbook documenting all running services.

## Scripts

All scripts are in `scripts/`. Run with `python3 <script>`. All output JSON to stdout.

| Script | Purpose |
|--------|---------|
| `scan_docker.py` | Running containers: name, image, ports, mounts, status |
| `scan_services.py` | System services via launchd (macOS) or systemd (Linux) |
| `scan_ports.py` | Open TCP listening ports with process and PID |
| `generate_runbook.py` | Combine all scans → formatted Markdown runbook |

## Generating a Runbook

**Quickest — run all scanners inline and print to stdout:**
```bash
python3 scripts/generate_runbook.py
```

**Save to a file:**
```bash
python3 scripts/generate_runbook.py --output ~/homelab-runbook.md
```

**Save to workspace:**
```bash
python3 scripts/generate_runbook.py --output /Users/openclaw/.openclaw/workspace/homelab-runbook.md
```

**Pre-collect then generate (useful for cron or piping):**
```bash
python3 scripts/scan_docker.py > /tmp/docker.json
python3 scripts/scan_services.py > /tmp/services.json
python3 scripts/scan_ports.py > /tmp/ports.json
python3 scripts/generate_runbook.py --docker /tmp/docker.json --services /tmp/services.json --ports /tmp/ports.json --output ~/homelab-runbook.md
```

## Agent Workflow

When the user asks for a homelab runbook or service inventory:

1. Run `generate_runbook.py` (all scanners inline, save to workspace file).
2. Read the output file and summarize key findings:
   - How many Docker containers are running and what they are
   - Notable open ports and the processes owning them
   - Any errors or warnings (Docker not found, permission denied, etc.)
3. Offer to save to Obsidian vault if the user wants it persisted.

Use the `--output` flag to write to the workspace. Do not dump the full raw Markdown at the user — summarize it and offer the file path.

## Edge Cases

- **Docker not installed:** `scan_docker.py` returns `{"error": "Docker not installed or not running", "containers": []}` — runbook shows a warning, continues.
- **No containers running:** Returns empty list, runbook shows "_No running containers._"
- **Port scan permission denied:** `scan_ports.py` returns an error — runbook shows warning. Tell the user to re-run with `sudo` if full port visibility is needed.
- **Linux without systemd:** `scan_services.py` will return an error — acceptable, runbook notes it.

## Customization

See `references/customization.md` for:
- Excluding specific services/containers/ports
- Adding manual service notes (URLs, config paths, restart commands)
- Scheduling with cron
- Modifying output format
