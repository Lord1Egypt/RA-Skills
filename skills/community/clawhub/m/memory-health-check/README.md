# 🩺 memory-health-check

> A proactive health diagnostic Skill for OpenClaw agents.

**Purpose:** Monitor memory integrity, detect corruption, identify bloat, flag orphaned entries, and provide actionable repair recommendations.

**Tagline:** *"An ounce of prevention is worth a pound of lost memories."*

---

## Features

| Dimension | What It Checks | Healthy | Warning | Critical |
|-----------|----------------|---------|---------|----------|
| **Integrity** | SQLite corruption, checksums | ✅ | ⚠️ | 🔴 |
| **Bloat** | Total size, file count | <500 MB | 500 MB–2 GB | >2 GB |
| **Orphans** | Entries with zero inbound `[[links]]` | 0% | 1–5% | >5% |
| **Dedup** | Duplicate / near-duplicate entries | <2% | 2–10% | >10% |
| **Freshness** | % updated in last 30 days | >70% | 40–70% | <40% |
| **Health Score** | Weighted aggregate 0–100 | ≥80 | 50–79 | <50 |

---

## Usage

```bash
# Full health check
~/.openclaw/workspace/skills/memory-health-check/bin/health_check.sh

# With auto-repair
~/.openclaw/workspace/skills/memory-health-check/bin/health_check.sh --auto-repair

# Specific dimensions only
~/.openclaw/workspace/skills/memory-health-check/bin/health_check.sh --dims bloat,freshness

# Run individual scripts directly
python3 ~/.openclaw/workspace/skills/memory-health-check/bin/bloat_detector.py
python3 ~/.openclaw/workspace/skills/memory-health-check/bin/integrity_scan.py --json
python3 ~/.openclaw/workspace/skills/memory-health-check/bin/freshness_report.py -v
```

---

## Architecture

```
bin/
  health_check.sh       # Main entry point
  integrity_scan.py     # SQLite corruption checks
  bloat_detector.py     # Size / file count analysis
  orphan_finder.py      # [[Obsidian link]] reference graph
  dedup_scanner.py      # Token-overlap duplicate detection
  freshness_report.py    # File age distribution
  health_score.py       # Aggregate scoring engine

scripts/
  generate_report.py     # JSON report → ~/.openclaw/workspace/memory/health-reports/
  auto_repair.py        # Orphan + temp file cleanup
```

---

## Auto-Repair Options

```bash
# Dry run (preview what would be deleted)
python3 scripts/auto_repair.py --dry-run

# Remove orphans (inbound-unlinked files)
python3 scripts/auto_repair.py --remove-orphans

# Skip specific cleanup types
python3 scripts/auto_repair.py --no-ds-store --no-empty
```
