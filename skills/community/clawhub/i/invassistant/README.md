# InvAssistant — Personal Investment Portfolio Management Framework

A WorkBuddy/CodeBuddy Skill implementing a multi-asset investment strategy framework. Covers US, A-share, and HK stocks with asset-class differentiated rules, portfolio-level risk controls, and disciplined execution protocols.

**Current version**: v2.3.1 (2026-06-06)

## What It Does

InvAssistant combines AI-driven strategy guidance with executable trading rules:

- **Asset Classification** — Three tiers (A: Platform Core / B: High-Beta Cyclical / C: Low-Volatility Income) with differentiated entry/exit logic
- **Portfolio Risk Controls** — 7 non-overridable red lines (single position ≤25%, sector ≤35%, AI narrative ≤50%, drawdown defense, VIX circuit breakers)
- **Multi-Market Coverage** — US stocks (A/B/C tiered), A-shares (3-condition engine), HK stocks (warning-line framework)
- **Entry Modes** — Mode A (panic mispricing), Mode B (trend confirmation), Mode C (rebalancing), Mode D (A-class candidate zone entry, v2.1.1)
- **QMS Scoring** — 4-factor quality rating (earnings trend, sector relative strength, EPS revision, price structure)

## Quick Start

```bash
cp -r invassistant-skill ~/.workbuddy/skills/invassistant
pip install -r requirements.txt
```

Then ask WorkBuddy: "检查持仓" or "portfolio check".

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v2.3.1 | 2026-06-06 | Major cleanup: English SKILL.md, clean frontmatter, bilingual README, no personal scripts |
| v2.1.1 | 2026-06-04 | Mode D: A-class candidate zone entry (no observation delay) |
| v2.1.1 | 2026-06-04 | Mode D: A-class candidate zone entry (no observation delay) |
| v2.1 | 2026-05-18 | A/B/C asset classification; 7 red lines; 4-factor QMS; trailing stop removed for A-class |
| v2.0 | 2026-05-18 | Full rebuild: decision pyramid, 5-factor QMS, 10 red lines (replaced by v2.1) |
| v1.5.x | 2026 Q1-Q2 | 3-condition engine, dual-mode entry, trailing stops, behavioral patches |
| v1.0 | 2026-01 | Initial: 3 red lines entry + multi-layer exit engine |

## Architecture

```
invassistant/
├── SKILL.md                    # Core definition (triggers, workflow, strategy rules)
├── README.md                   # This file (English)
├── README_zh.md                # Chinese documentation
├── references/                 # Detailed strategy references
│   ├── us_stock_strategy.md    # US stock A/B/C rules + Mode D
│   ├── a_share_strategy.md     # A-share 3-condition engine
│   └── risk_control_and_overrides.md  # 7 red lines, QMS, override protocol
└── scripts/                    # Execution engine (Python)
    ├── portfolio_checker.py    # Main checker
    ├── redline_engine.py       # Entry filter engine
    ├── exit_engine.py          # Exit engine (stop-loss, trend break, momentum)
    └── send_*.py               # Push to WeChat/DingTalk/Feishu
```

## License

MIT License — see [LICENSE](LICENSE)
