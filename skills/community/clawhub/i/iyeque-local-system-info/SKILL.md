---
name: local-system-info
description: "Agent-ready local diagnostics for CPU, memory, disk, load, and bounded process inspection. Use for capacity checks, troubleshooting, and deciding whether a local task has enough resources."
license: MIT-0
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins: ["python3"]
      pip: ["psutil"]
    version: "1.2.2"
---

# Local system diagnostics

Use `sysinfo.py` for read-only, local-only health checks. It does not send metrics anywhere or modify the system. Process results expose process names and resource values by default. Usernames are excluded by default and require the explicit `--include-owners` flag only when owner attribution is necessary.

```bash
uv run --with psutil sysinfo.py summary
uv run --with psutil sysinfo.py cpu
uv run --with psutil sysinfo.py memory
uv run --with psutil sysinfo.py disk
uv run --with psutil sysinfo.py processes --limit 10
```

Actions are `summary`, `cpu`, `memory`, `disk`, and `processes`. Output is JSON. Process limits are bounded from 1 to 100; use `--include-owners` only for an explicit owner-attribution request. Load averages are normalized by logical CPU count where the platform provides them; Windows may return an empty list.

Use `summary` before expensive local work, `memory` and `disk` before model/PDF/audio jobs, and `processes` when diagnosing contention. Treat values as a point-in-time observation rather than a continuous monitor.

## Source and support

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/local-system-info

Report bugs and security concerns through the repository issue guidance.
