# Homelab Runbook — Customization Guide

## Excluding Services or Containers

To exclude specific items from the runbook, edit the relevant scan script and add a filter:

**Skip a Docker container by name:**
```python
# In scan_docker.py, inside scan_docker(), after building containers list:
EXCLUDE_CONTAINERS = {"watchtower", "portainer"}
containers = [c for c in containers if c["name"] not in EXCLUDE_CONTAINERS]
```

**Skip launchd services matching a pattern (macOS):**
```python
# In scan_services.py, after building services list:
import re
EXCLUDE_PATTERNS = [r"^com\.apple\.", r"^com\.google\."]
services = [s for s in services if not any(re.match(p, s["name"]) for p in EXCLUDE_PATTERNS)]
```

**Skip ports:**
```python
# In scan_ports.py, after building ports list:
EXCLUDE_PORTS = {631, 5353}  # e.g., CUPS, mDNS
ports = [p for p in ports if p["port"] not in EXCLUDE_PORTS]
```

---

## Adding Manual Service Notes

The runbook Markdown is plain text — you can add a section at the bottom manually, or extend `generate_runbook.py` to read a notes file:

**Example notes file** (`~/.homelab-notes.json`):
```json
{
  "plex": {
    "url": "http://192.168.1.10:32400",
    "config": "~/Library/Application Support/Plex Media Server",
    "notes": "Media server. Restart with: launchctl kickstart -k gui/501/tv.plex.plexmediaserver"
  },
  "pihole": {
    "url": "http://192.168.1.2/admin",
    "notes": "DNS ad-blocker. Admin password in Bitwarden."
  }
}
```

**In `generate_runbook.py`**, add after `section_ports()`:
```python
import pathlib

def section_notes():
    notes_path = pathlib.Path.home() / ".homelab-notes.json"
    if not notes_path.exists():
        return []
    with open(notes_path) as f:
        notes = json.load(f)
    lines = ["## 📝 Manual Service Notes", ""]
    for name, info in notes.items():
        lines.append(f"### {name}")
        if "url" in info:
            lines.append(f"- **URL:** {info['url']}")
        if "config" in info:
            lines.append(f"- **Config:** `{info['config']}`")
        if "notes" in info:
            lines.append(f"- **Notes:** {info['notes']}")
        lines.append("")
    return lines
```

---

## Scheduling with Cron

To auto-generate and save a fresh runbook daily:

```cron
# Generate runbook every day at 6am, save to workspace
0 6 * * * /usr/bin/python3 /Users/openclaw/.openclaw/workspace/skills/homelab-runbook/scripts/generate_runbook.py --output /Users/openclaw/.openclaw/workspace/homelab-runbook.md 2>/dev/null
```

Or use the OpenClaw cron system to trigger via the agent skill.

---

## Customizing the Output Format

`generate_runbook.py` produces GitHub-flavored Markdown. To change output:

- **Add a title or header** — edit the `generate_runbook()` function's `lines` preamble.
- **Change date format** — modify the `ts` format string: `now.strftime(...)`.
- **Skip a section** — comment out the relevant `lines +=` call.
- **Add emoji / change headers** — edit the `section_*()` functions directly.

---

## Running with Pre-Collected Data

Collect scan data once, run the generator multiple times without re-scanning:

```bash
python3 scan_docker.py > docker.json
python3 scan_services.py > services.json
python3 scan_ports.py > ports.json

python3 generate_runbook.py --docker docker.json --services services.json --ports ports.json --output runbook.md
```
