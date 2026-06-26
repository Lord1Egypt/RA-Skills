---
name: ocas-rally
source: https://github.com/indigokarasu/rally
install: openclaw skill install https://github.com/indigokarasu/rally
description: Use when researching, scoring, planning allocations, or generating trade plans for public markets. Handles universe screening, signal scoring, constrained allocation, rebalance planning, and auditable investment decisions. Long-only by default. Trigger phrases: 'portfolio', 'allocation', 'rebalance', 'trade plan', 'research stocks', 'daily report', 'market signals', 'update rally'. Do not use for meme-stock speculation, margin trading, or budget planning.
metadata: {"openclaw":{"emoji":"📊"}}
---

# Rally

Rally turns public-market research into explainable, risk-bounded allocation and trade plans — screening a universe of candidates, computing composite signals, and solving for constrained allocations that respect hard limits including long-only positioning, max position size, and maximum drawdown. Execution is disabled by default, so Rally is fully useful as a research and planning tool even without brokerage integration.


## When to use

- Research and rank an investable universe
- Generate constrained allocation plans from ranked candidates
- Derive trade plans from current-vs-target deltas
- Run daily or monthly portfolio reporting
- Validate portfolio state against risk constraints


## When not to use

- Meme-stock speculation or hype-driven picks
- Margin, shorting, or leveraged products (unless explicitly enabled)
- Budget or personal finance planning
- Generic financial news summarization — use Sift


## Responsibility boundary

Rally owns governed portfolio research, scoring, allocation, and trade planning.

Rally does not own: general web research (Sift), knowledge graph (Elephas), communications (Dispatch), pattern analysis (Corvus).


## Commands

- `rally.ingest.portfolio` — ingest or update portfolio state
- `rally.universe.refresh` — rebuild the investable universe with filters
- `rally.research.signals` — compute signals and composite rankings
- `rally.candidates.rank` — ranked candidate list with scores
- `rally.plan.allocation` — constrained allocation plan
- `rally.plan.trade` — trade plan from current-vs-target deltas
- `rally.execute.trades` — execute trades (disabled by default)
- `rally.report.daily` — daily portfolio report
- `rally.report.monthly` — monthly performance attribution
- `rally.validate` — run risk and constraint validation checks
- `rally.status` — portfolio summary, active plan, risk check status
- `rally.journal` — write journal for the current run; called at end of every run
- `rally.update` — pull latest from GitHub source; preserves journals and data


## Run completion

After every Rally command:

1. Persist portfolio state, research events, signals, plans to local JSONL files
2. Log material decisions (allocation changes, trade plans) to `decisions.jsonl`
3. Write journal via `rally.journal` — Observation Journal for research/scoring runs, Action Journal for trade execution runs

## Hard boundaries

- Long-only unless explicitly configured otherwise
- No margin, shorting, leverage, or derivatives unless enabled
- No assumed external deposits — growth from returns and reallocation only
- Execution disabled by default and never required for the skill to be useful
- Every target has rationale and evidence references
- Risk check failure halts the plan


## Storage layout

```
~/openclaw/data/ocas-rally/
  config.json
  portfolio_state.jsonl
  research_events.jsonl
  signals.jsonl
  decisions.jsonl
  allocation_plans.jsonl
  trade_plans.jsonl
  wash_sale_exclusions.jsonl
  factor_ic.jsonl
  congressional_flow_cache.jsonl
  reports/

~/openclaw/journals/ocas-rally/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-rally",
  "skill_version": "3.0.0",
  "config_version": "2",
  "created_at": "",
  "updated_at": "",
  "benchmark": "SPY",
  "execution": {
    "enabled": false,
    "broker_integration": null
  },
  "constraints": {
    "long_only": true,
    "max_position_pct": 0.15,
    "max_sector_pct": 0.30,
    "max_drawdown": 0.10,
    "max_pairwise_corr": 0.85,
    "corr_lookback_days": 60,
    "corr_penalty_factor": 0.50
  },
  "cash": {
    "normal_pct": 0.05,
    "cautious_pct": 0.15,
    "defensive_pct": 0.30
  },
  "universe": {
    "min_market_cap_bn": 2.0,
    "min_adv_mn": 5.0,
    "target_positions": 15,
    "include_foreign": false
  },
  "position_sizing": "score_vol_weighted",
  "position_sizing_options": {
    "vol_lookback_days": 60,
    "vol_min_days": 20,
    "floor_pct": 0.02,
    "cap_pct": 0.15
  },
  "scoring": {
    "quality_weight": 0.40,
    "momentum_weight": 0.20,
    "safety_weight": 0.25,
    "reversion_weight": 0.10,
    "congressional_flow_weight": 0.05,
    "reversion_lookback_days": 5,
    "confidence_floor": 0.40,
    "sector_blend_weight": 0.50,
    "min_sector_size": 5
  },
  "regime": {
    "signals": ["trend", "credit", "volatility", "breadth"],
    "weights": [0.25, 0.25, 0.25, 0.25],
    "thresholds": {
      "normal_floor": 0.65,
      "cautious_floor": 0.40
    },
    "elevated_confidence_floor": 0.55,
    "trend": {
      "sma_days": 200
    },
    "credit": {
      "source": "HY_OAS",
      "bullish_ceiling_bp": 350,
      "bearish_floor_bp": 500
    },
    "volatility": {
      "metric": "VIX_TERM_STRUCTURE",
      "contango_threshold_pct": 5.0
    },
    "breadth": {
      "index": "SP500",
      "ma_days": 50,
      "bullish_floor_pct": 65,
      "bearish_ceiling_pct": 40
    },
    "reentry_deploy_max_pct": 0.50
  },
  "earnings_overlay": {
    "enabled": true,
    "lookahead_trading_days": 5,
    "reduce_pct": 0.50,
    "hold_through_percentile": 0.80
  },
  "rebalance": {
    "drift_threshold": 0.05,
    "min_interval_days": 14,
    "displacement_threshold": 0.35,
    "max_turnover_pct": 0.30,
    "emergency_drop_pct": 0.15,
    "atr_stop_multiplier": 3.0,
    "atr_lookback_days": 14,
    "stop_type": "dual",
    "cost_aware_turnover": true,
    "estimated_cost_model": "adv_based"
  },
  "drawdown_risk_budget": {
    "enabled": true,
    "trailing_days": 20,
    "reduction_threshold_pct": -0.08,
    "reduction_factor": 0.25,
    "recovery_requires_regime_normal": true
  },
  "factor_monitor": {
    "enabled": true,
    "ic_lookback_runs": 30,
    "alert_threshold_ic": 0.0,
    "alert_consecutive_days": 60
  },
  "congressional_flow": {
    "enabled": true,
    "api_source": "quiverquant",
    "api_key_env_var": "QUIVERQUANT_API_KEY",
    "flow_lookback_days": 30,
    "committee_relevance_multiplier": 1.5,
    "cluster_threshold": 3,
    "cluster_bonus_multiplier": 1.5,
    "max_data_age_days": 3
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```


## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: decision_accuracy
    metric: fraction of allocation decisions outperforming benchmark over evaluation window
    direction: maximize
    target: 0.60
    evaluation_window: 30_runs
  - name: risk_adjusted_return
    metric: Sharpe ratio relative to benchmark
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: max_drawdown
    metric: maximum portfolio drawdown from peak
    direction: minimize
    target: 0.10
    evaluation_window: 30_runs
```


## Optional skill cooperation

- Sift — web research for signal enrichment
- Vesper — emits portfolio outcome signals for briefings


## Journal outputs

- Observation Journal — research and scoring runs
- Action Journal — trade execution runs


## Initialization

On first invocation of any Rally command, run `rally.init`:

1. Create `~/openclaw/data/ocas-rally/` and subdirectories (`reports/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `portfolio_state.jsonl`, `research_events.jsonl`, `signals.jsonl`, `decisions.jsonl`, `allocation_plans.jsonl`, `trade_plans.jsonl`, `wash_sale_exclusions.jsonl`, `factor_ic.jsonl`, `congressional_flow_cache.jsonl`
4. Create `~/openclaw/journals/ocas-rally/`
5. Register cron jobs `rally:daily` and `rally:update` if not already present (check `openclaw cron list` first)
6. Log initialization as a DecisionRecord in `decisions.jsonl`


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `rally:daily` | cron | `0 6 * * 1-5` (weekdays 6am) | Full daily sequence: universe refresh, update stops, check emergency sells, fetch congressional data, compute signals, regime score, drawdown check, factor monitor, rebalance triggers, (if triggered: earnings overlay, correlation penalty, allocation, turnover budget, trade plan), daily report, journal |
| `rally:update` | cron | `0 0 * * *` (midnight daily) | `rally.update` |

Cron options: `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

Registration during `rally.init`:
```
openclaw cron list
# If rally:daily absent:
openclaw cron add --name rally:daily --schedule "0 6 * * 1-5" --command "rally.universe.refresh && rally.research.signals && rally.report.daily && rally.journal" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If rally:update absent:
openclaw cron add --name rally:update --schedule "0 0 * * *" --command "rally.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`rally.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from `skill.json`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/skill.json" --jq '.content' | base64 -d | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Rally from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/data-model.md` | Before creating portfolio state, candidates, or plans |
| `references/research-and-scoring.md` | Before universe filtering, signal computation, or scoring |
| `references/operating-model.md` | Before running the full ingest-to-report loop |
| `references/journal.md` | Before rally.journal; at end of every run |
