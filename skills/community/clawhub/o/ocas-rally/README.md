# 📊 Rally

Rally turns public-market research into explainable, risk-bounded allocation and trade plans -- screening a universe of candidates, computing composite signals, and solving for constrained allocations that respect hard limits including long-only positioning, max position size, and maximum drawdown. Execution is disabled by default, so Rally is fully useful as a research and planning tool even without brokerage integration.

---

## Overview

Rally brings discipline to portfolio management -- not stock-picking tips, but a governed workflow for turning public-market research into explainable, risk-bounded allocation and trade plans. It screens a universe of candidates, computes composite signals from multiple sources, and solves for constrained allocations that respect hard limits including long-only positioning, max position size, and maximum drawdown. Execution is disabled by default, making Rally fully useful as a research and planning tool even without live brokerage access. Every target has rationale and evidence references, and risk check failure halts the plan.

## Commands

| Command | Description |
|---|---|
| `rally.ingest.portfolio` | Ingest or update portfolio state |
| `rally.universe.refresh` | Rebuild the investable universe with filters |
| `rally.research.signals` | Compute signals and composite rankings |
| `rally.candidates.rank` | Ranked candidate list with scores |
| `rally.plan.allocation` | Constrained allocation plan |
| `rally.plan.trade` | Trade plan from current-vs-target deltas |
| `rally.execute.trades` | Execute trades (disabled by default) |
| `rally.report.daily` | Daily portfolio report |
| `rally.report.monthly` | Monthly performance attribution |
| `rally.validate` | Run risk and constraint validation checks |
| `rally.status` | Portfolio summary, active plan, risk check status |
| `rally.journal` | Write journal for the current run |
| `rally.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`rally.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. It also registers the `rally:daily` cron job (weekdays 6am) and `rally:update` (midnight daily, self-update). No manual setup is required.

## Dependencies

**OCAS Skills**
- [Sift](https://github.com/indigokarasu/sift) -- web research for signal enrichment
- [Vesper](https://github.com/indigokarasu/vesper) -- receives portfolio outcome signals for briefings

**External**
- Brokerage API (optional, for trade execution -- disabled by default)

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `rally:daily` | cron | `0 6 * * 1-5` (weekdays 6am) | Universe refresh, signal computation, daily report |
| `rally:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v3.0.1 -- March 27, 2026
- Added `rally.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Run completion with state persistence and journaling
- Cron registration for daily market pass

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Rally is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
