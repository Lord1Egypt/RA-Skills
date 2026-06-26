# 🩺 memory-health-check

> **Version:** 1.0.0  
> **Skill ID:** `memory-health-check`  
> **Status:** Ready for Development

## Quick Reference

| 项目 | 内容 |
| ---- | ---- |
| 核心功能 | 6维内存健康诊断（完整性/新鲜度/膨胀率/孤儿/去重/覆盖率） |
| 主入口 | `bin/health_check.sh` |
| 依赖 | OpenClaw v2026.4.9+, sqlite3 |

## Features (MVP)

1. **Integrity scan** — DB corruption / checksum checks
2. **Bloat detection** — DB size, file count, growth rate
3. **Orphan detection** — Entries with zero inbound references
4. **Freshness report** — Entry age distribution
5. **Dedup scanner** — Duplicate / near-duplicate entries
6. **Health score** — Aggregate 0–100 score across all dimensions
7. **Auto-repair** — Orphan cleanup on user approval

## File Structure

```
memory-health-check/
├── SKILL.md                   # This file
├── bin/
│   ├── health_check.sh        # Main entry point
│   ├── integrity_scan.py      # DB corruption checks
│   ├── bloat_detector.py      # Size analysis
│   ├── orphan_finder.py       # Reference graph orphan detection
│   ├── dedup_scanner.py       # Duplicate detection
│   ├── freshness_report.py     # Entry age distribution
│   └── health_score.py         # Aggregate scoring
├── scripts/
│   ├── generate_report.py      # Report generator
│   └── auto_repair.py         # Cleanup script
├── config/
│   └── thresholds.yaml
├── reports/
│   └── .gitkeep
└── README.md
```

## Usage

```bash
# Full health check
memory-health-check/bin/health_check.sh

# With auto-repair
memory-health-check/bin/health_check.sh --auto-repair

# Specific dimensions only
memory-health-check/bin/health_check.sh --dims integrity,bloat
```

## Health Score Dimensions

| Dimension | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Integrity | ✅ | ⚠️ | 🔴 |
| Freshness (>70%) | >70% | 40–70% | <40% |
| Bloat | <500MB | 500MB–2GB | >2GB |
| Orphans | 0% | 1–5% | >5% |
| Dedup | <2% | 2–10% | >10% |
| Coverage | >80% | 50–80% | <50% |

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1 scan/week, text report |
| **Pro** | **$9.90/mo** | Unlimited scans, 6-dim diagnostics, auto-repair, 90-day history |
| Bundle | **$17.90/mo** | dreaming-optimizer Pro + memory-health-check Pro |

## Development

See: ``
