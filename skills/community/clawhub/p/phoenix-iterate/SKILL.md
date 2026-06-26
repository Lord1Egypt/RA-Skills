---
name: phoenix-iterate
description: AI-driven quantitative strategy iteration workflow — a complete loop of briefing, hypothesis, code generation, constitutional scan, backtest submission, forensic diagnosis, and lesson recording for QuantConnect strategies.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      skills:
        - backtest-poller
        - qc-deep-feature-forensics
    emoji: "\U0001F525"
---

# Phoenix Iterate

A structured workflow for AI-assisted quantitative strategy iteration. Instead of randomly tweaking code, this skill enforces a disciplined loop: read history, form hypothesis, write code, validate against past mistakes, backtest progressively, diagnose results, and record lessons.

## Dependencies

This skill is an **orchestrator** — it coordinates two companion skills that must be installed separately:

| Skill | Purpose | Commands provided |
|-------|---------|------------------|
| `backtest-poller` | Backtest submission, monitoring, early-stop, results | `cli.py submit/status/results/logs` |
| `qc-deep-feature-forensics` | Deep feature-level forensic analysis | `deep_forensics.py` |

Install them first:
```bash
clawhub install backtest-poller
clawhub install qc-deep-feature-forensics
```

All `cli.py` references below assume `backtest-poller` is installed as a sibling directory (`../backtest-poller/cli.py`). Adjust the path if your install location differs.

## When to use

- "Let's iterate on the strategy"
- "Start a new strategy version"
- "Run the phoenix iteration loop"
- "What should I try next?"

## The Iteration Loop

```
Step 1: Briefing     ──> Read constitutional memory + history
Step 2: Hypothesis   ──> Pick ONE mutation dimension, form testable hypothesis
Step 3: Code         ──> Write strategy, scan for violations
Step 4: Submit       ──> Progressive validation (smoke -> stress -> medium -> full)
Step 5: Diagnose     ──> Run forensics on results
Step 6: Record       ──> Update constitutional memory with new lessons
         |
         └──────────> Loop back to Step 1
```

### Step 1: Get Decision Context

```bash
python3 orchestrator.py briefing
```

Returns:
- Constitutional memory (all past lessons sorted by severity)
- Available strategy blueprints with historical performance
- Mutation dimensions (what can be changed)
- Recent iteration history (what was tried, what happened)
- Resource constraints and validation windows

### Step 2: Form a Trading Hypothesis

Before writing code, answer these questions:
1. **What am I changing?** — Pick exactly one mutation dimension
2. **Why do I think this will be better?** — Based on data, not intuition
3. **What if I'm wrong?** — Worst case scenario, does it violate any iron laws?
4. **Will this affect trade frequency?** — If trades decrease, there must be a compensating mechanism

**Mutation Dimensions:**

| Dimension | Description | Examples |
|-----------|-------------|---------|
| `survival_structure` | How the strategy survives downturns | QQQ buy-and-hold, cash defense, SMA filter |
| `position_sizing` | How much capital per trade | Kelly %, max trade value, total exposure cap |
| `selection` | What stocks to trade | Premarket volume, RS breakout, HV lottery |
| `profit_management` | What to do with winners | Hold to expiry, take-profit at 200%, trailing stop |

### Step 3: Write & Scan Code

1. Create a new strategy directory: `strategies/M{N}_{description}/main.py`
2. Base it on the latest passing version
3. Run constitutional scan:

```bash
python3 orchestrator.py scan --code strategies/M31_test/main.py
```

If violations are found, fix them before submitting.

### Step 4: Progressive Validation

Submit through increasingly demanding test windows. Only promote to the next stage after passing.

```
Stage 1: Smoke Test  (3 months,  ~15min)  DD < 50%  — Catch obvious bugs
Stage 2: Stress Test (5 months,  ~30min)  DD < 45%  — Survive worst conditions
Stage 3: Medium      (18 months, ~1hr)    DD < 42%  — Bull/bear transitions
Stage 4: Full        (3 years,   ~3hr)    DD < 40%  — Final acceptance
```

```bash
# Check no active backtests  (backtest-poller skill)
python3 ../backtest-poller/cli.py status

# Submit with early-stop protection
python3 ../backtest-poller/cli.py submit \
  --backtest-id <id> \
  --name "MyStrategy_smoke" \
  --max-dd 50

# Monitor progress
python3 ../backtest-poller/cli.py status

# View results when done
python3 ../backtest-poller/cli.py results --name "MyStrategy_smoke" --full
```

**Shortcut**: If you only changed profit management (not entry logic), you can skip Smoke/Stress and start from Medium.

### Step 5: Diagnose

```bash
python3 orchestrator.py diagnose \
  --orders results/MyStrategy_smoke/xxx_orders.csv \
  --result results/MyStrategy_smoke/xxx_result.json
```

For deeper analysis, run the feature forensics (requires `qc-deep-feature-forensics` skill):
```bash
python3 ../qc-deep-feature-forensics/deep_forensics.py results/MyStrategy_smoke/xxx_orders.csv
```

### Step 6: Record & Decide

```bash
python3 orchestrator.py record \
  --name "MyStrategy_v2" \
  --blueprint "baseline" \
  --dimension "position_sizing" \
  --hypothesis "Reduce position size to 2% for better survival" \
  --window "smoke_test" \
  --status "completed" \
  --sharpe 1.5 \
  --drawdown 0.35 \
  --net-profit 0.85
```

**Decision Matrix:**

| Outcome | Action |
|---------|--------|
| Current stage passed | Change dates to next stage, resubmit |
| DD exceeded but promising | Analyze monthly cashflow, find bleeding point, targeted fix |
| Too few trades | **Red flag** — loosen entry conditions or shorten cooldown |
| Sharpe < 1.0 but DD ok | Acceptable for now, optimize Sharpe later |
| Full period passed | Strategy qualified! |

## Quick Reference

```bash
# This skill (orchestrator)
python3 orchestrator.py briefing          # Decision context
python3 orchestrator.py status             # System status
python3 orchestrator.py list               # Available strategies
python3 orchestrator.py scan --code <path> # Code violation check

# backtest-poller skill
python3 ../backtest-poller/cli.py status                      # Backtest status
python3 ../backtest-poller/cli.py logs --lines 30             # Poller logs
python3 ../backtest-poller/cli.py results --name <name> --full # View results

# qc-deep-feature-forensics skill
python3 ../qc-deep-feature-forensics/deep_forensics.py <orders.csv>  # Deep forensics
```

## Rules

- **Only 1 backtest can run at a time** (serial execution). Never submit a second backtest while one is running.
- **Full-period backtests take 2-3 hours** — always use progressive validation to fail fast. Do not jump directly to full-period.
- **Always run `scan_strategy()` before submitting.** Constitutional violations must be resolved before backtest submission. Do not bypass the scanner.
- **Each iteration must change exactly one mutation dimension.** Changing multiple variables at once makes it impossible to attribute success or failure to a specific change.
- **Record every iteration result**, including failures. Unrecorded iterations will be lost and the same mistake may be repeated.
- **The poller daemon handles monitoring automatically** after submission. Do not poll the QC API manually — let the daemon manage state.
