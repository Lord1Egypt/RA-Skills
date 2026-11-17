
A WorkBuddy/CodeBuddy Skill implementing a multi-asset investment strategy framework. Covers US, A-share, and HK stocks with asset-class differentiated rules, portfolio-level risk controls, and disciplined execution protocols.

**Current version**: v2.3.19 (2026-09-20)

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

> ⚠️ **Data transmission notice**: the optional `scripts/send_*.py` helpers push report content to a webhook endpoint that you configure (WeCom / DingTalk / Feishu). They are inert until configured and never send anything else. Review your endpoint config before enabling.

> ⚠️ **Not financial advice**: this is a decision-support framework. All outputs require human review; the author assumes no liability for trading losses.

## Version History

Recent releases only. **[CHANGELOG.md](CHANGELOG.md)** is authoritative and carries the complete history.

| Version | Date | Key Changes |
|---------|------|-------------|
| v2.3.19 | 2026-09-20 | LP1 fix: frontmatter `permissions` block added (quote endpoint, webhook URLs, notification credential env-var names) + `network` token in `allowed-tools` — declaring the outbound behaviors the body already disclosed; data-transmission notice corrected |
| v2.3.17 | 2026-09-17 | Restructure: §12 and §13 moved to `references/capital_plan_audit.md` and `references/derived_price_governance.md`, leaving the operating spine inline (the five-step loop, what a clean validator run does not tell you, the A1-A5 detection table). No rule text deleted — all of it relocated verbatim and cross-linked from §12/§13 and from the Reference Files table. Splitting so that the always-read file does not have to be skimmed, which is the same failure mode D10 addresses inside a registry |
| v2.3.16 | 2026-09-17 | Add D9 (an unsettled question needs its own ledger — one absorptive register, a per-entry blocking scope, adjudication deliberately outside pass/fail, mirrors that replicate values but not disputes) + D10 (keep the registry executable and move chronology to a companion file; guard the shape, not only the size; derive size targets from a measured floor) + the "a green validator is not an action permit" rule in D4 + mistakes P11/P12 |
| v2.3.15 | 2026-09-16 | Hardening per scanner findings: valuation gate + volume confirmation fail-closed in `redline_engine.py`; Framework Scope and Bundled Scripts section; allowed-tools completion; data-transmission notices; pinned requirements |
| v2.3.14 | 2026-09-11 | Add D8 (example configs carry no author positions — sample tickers must be generic and must never coincide with real holdings, because a shipped example that mirrors your book is a disclosure, not a demo) + P10; purged real tickers from `scripts/init_config.py` sample watchlist and from two inline code comments |

## Architecture

```
invassistant/
├── SKILL.md                    # Core definition (triggers, workflow, strategy rules)
├── README.md                   # This file (English)
├── README_zh.md                # Chinese documentation
├── CHANGELOG.md                # Complete release history (authoritative)
├── references/                 # Detailed strategy references
│   ├── us_stock_strategy.md    # US stock A/B/C rules + Mode D
│   ├── a_share_strategy.md     # A-share 3-condition engine
│   ├── risk_control_and_overrides.md  # 7 red lines, QMS, override protocol
│   ├── candidate_admission_gates.md   # G0-G5 admission gates, S6 water level
│   ├── capital_plan_audit.md   # Multi-sleeve capital plan audit (A1-A5)
│   └── derived_price_governance.md    # Derived price-level governance (D1-D10)
└── scripts/                    # Execution engine (Python, optional helpers)
    ├── portfolio_checker.py    # Main checker
    ├── redline_engine.py       # Entry filter engine (fail-closed gates)
    ├── exit_engine.py          # Exit engine (stop-loss, trend break, momentum)
    ├── init_config.py          # First-run config generator (generic sample tickers)
    ├── data_fetcher.py         # Market-data fetch helper
    └── send_*.py               # Opt-in push to WeCom/DingTalk/Feishu webhooks
```

## License

MIT License — see [LICENSE](LICENSE)
