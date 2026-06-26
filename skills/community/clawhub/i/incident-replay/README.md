# Incident Replay — Agent Failure Forensics

**Post-mortem analysis for AI agent failures. Capture state, reconstruct timelines, identify root causes.**

When your agent breaks, you need to know what happened, why, and how to prevent it next time. Incident Replay captures workspace state at points in time, detects when things go wrong, reconstructs the sequence of events, and classifies root causes with actionable remediation steps.

---

## The Problem

Your agent crashed overnight. Files are missing. The config looks wrong. The logs are a wall of text. What happened? When? Why?

Without forensics tooling, post-mortem analysis is manual detective work: diffing files by hand, grepping logs, guessing at causation. Incident Replay automates the mechanics so you can focus on understanding.

## What It Does

### 1. **Capture** (`incident_capture.py`)
- Take point-in-time snapshots of your workspace (files, sizes, hashes, content)
- Configurable include/exclude patterns (track what matters, ignore noise)
- Automatic snapshot pruning (keep last N)
- Compare any two snapshots to see exactly what changed
- Trigger detection — automatically flag incidents based on:
  - Log patterns (tracebacks, errors, fatal messages)
  - File changes (unexpected deletions, config modifications)
  - Content patterns (secrets in output, constraint violations)
  - Empty output files

### 2. **Replay** (`incident_replay.py`)
- Build chronological timelines from snapshots, file changes, and triggers
- Extract decision chains from agent logs and memory files
- Heuristic root cause classification:
  - **Config error** — misconfiguration caused the failure
  - **Data corruption** — input data was malformed or missing
  - **Drift** — gradual workspace state degradation
  - **External failure** — API/network/filesystem dependency failed
  - **Logic error** — bug in agent logic or prompt
  - **Resource exhaustion** — ran out of memory, disk, tokens, or time
- Remediation suggestions tailored to each root cause category
- Incident database with persistent storage and pattern tracking

### 3. **Report** (`incident_report.py`)
- Full incident reports with timeline, changes, triggers, and remediation
- Summary reports across all incidents with severity and root cause breakdowns
- Decision chain visualisation (what the agent decided and why)
- Export markdown or JSON

---

## Quick Start

```bash
# 1. Configure
cp config_example.json incident_config.json
# Edit workspace root, triggers, log patterns

# 2. Take a baseline snapshot
python3 incident_capture.py --config incident_config.json --snapshot --label baseline

# 3. ... agent does work, something breaks ...

# 4. Take a post-incident snapshot
python3 incident_capture.py --config incident_config.json --snapshot --label post-incident

# 5. See what changed
python3 incident_capture.py --config incident_config.json \
  --diff incident_data/snapshots/SNAP1.json incident_data/snapshots/SNAP2.json

# 6. Check triggers
python3 incident_capture.py --config incident_config.json \
  --triggers incident_data/snapshots/SNAP1.json incident_data/snapshots/SNAP2.json

# 7. Full analysis — creates an incident with timeline, root cause, remediation
python3 incident_replay.py --config incident_config.json \
  --analyze incident_data/snapshots/SNAP1.json incident_data/snapshots/SNAP2.json \
  --title "Agent crashed during deployment"

# 8. Generate incident report
python3 incident_report.py --config incident_config.json --incident INC-0001

# 9. View all incidents and patterns
python3 incident_replay.py --config incident_config.json --incidents
python3 incident_replay.py --config incident_config.json --patterns
python3 incident_report.py --config incident_config.json --summary
```

## Programmatic Usage

```python
from incident_capture import Capturer, Snapshot, _load_config
from incident_replay import Analyzer

cfg = _load_config("incident_config.json")
cap = Capturer(cfg)
analyzer = Analyzer(cfg)

# Take snapshots
before = cap.take_snapshot(label="before")
# ... agent runs ...
after = cap.take_snapshot(label="after")

# Analyse
changes = cap.diff_snapshots(before, after)
triggers = cap.check_triggers(before, after)
decisions = analyzer.extract_decisions(after)
timeline = analyzer.build_timeline(
    [before, after],
    triggers=[t.to_dict() for t in triggers],
    changes=changes,
)

# Create incident
incident = analyzer.create_incident(
    title="Agent failed during task X",
    timeline=timeline,
    triggers=[t.to_dict() for t in triggers],
    file_changes=changes,
    decisions=decisions,
)
print(f"Created {incident.id}: {incident.root_cause}")
```

---

## Use Cases

- **Overnight failure analysis:** Agent ran unattended and broke — what happened?
- **Config change impact:** Track exactly what changed after a config update
- **Drift detection:** Compare weekly snapshots to catch gradual degradation
- **Secret leak detection:** Catch credentials or sensitive data in agent outputs
- **Regression forensics:** Agent used to work, now it doesn't — find the divergence point
- **Team incident management:** Track incidents over time, find recurring patterns

## What's Included

| File | Purpose |
|------|---------|
| `incident_capture.py` | State snapshot and change detection |
| `incident_replay.py` | Timeline reconstruction, analysis, incident management |
| `incident_report.py` | Report generation (markdown, JSON) |
| `config_example.json` | Full configuration template |
| `LIMITATIONS.md` | What this tool doesn't do |
| `LICENSE` | MIT License |

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works on any OS
- Platform-agnostic (works with any file-based AI agent workspace)

## Configuration

See `config_example.json` for the complete reference. Key areas:

- **`WORKSPACE_ROOT`** — Directory to monitor
- **`INCLUDE/EXCLUDE_PATTERNS`** — What files to capture
- **`TRIGGERS`** — Conditions that flag incidents (log patterns, file changes, content scans)
- **`ROOT_CAUSE_CATEGORIES`** — Classification categories with descriptions and remediation
- **`DECISION_MARKERS`** — Regex patterns to extract agent decisions from logs
- **`LOG_FILES`** — Which files to scan for decision chains

---

## quality-verified


## License

MIT — See `LICENSE` file.


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

------

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
