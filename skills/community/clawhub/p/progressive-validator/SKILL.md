---
name: progressive-validator
description: Multi-stage backtest validation framework — fail fast with short windows (smoke/stress/medium/full) before committing to expensive full-period backtests, saving hours of compute time.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F3AF"
---

# Progressive Validator

Stop wasting 3 hours on a backtest that was doomed from the start. This skill implements a multi-stage validation pipeline that eliminates bad strategies in 15 minutes instead of 3 hours.

## When to use

- "Validate this strategy"
- "Run the progressive test pipeline"
- "Is this strategy worth a full backtest?"
- When planning the validation sequence for a new strategy variant

## The Pipeline

```
     15 min                30 min               1 hour              3 hours
  +-----------+       +-----------+       +-----------+       +-----------+
  |   SMOKE   | pass  |  STRESS   | pass  |  MEDIUM   | pass  |   FULL    |
  |  3 months |------>|  5 months |------>| 18 months |------>|  3 years  |
  |  DD < 50% |       |  DD < 45% |       |  DD < 42% |       |  DD < 40% |
  +-----------+       +-----------+       +-----------+       +-----------+
       | fail              | fail              | fail              | fail
       v                   v                   v                   v
    REJECT              REJECT              REJECT              REJECT
   (15 min lost)      (45 min lost)       (1.5h lost)        (3h+ lost)
```

**Without progressive validation**: Every failed strategy costs 3 hours.
**With progressive validation**: Most failures caught in 15-45 minutes.

## Validation Stages

### Stage 1: Smoke Test
- **Period**: 2024-01-01 to 2024-03-31 (3 months)
- **Time**: ~15-20 minutes
- **Threshold**: Drawdown < 50%
- **Purpose**: Catch compilation errors, logic bugs, and catastrophic structural flaws
- **What it covers**: Q1 2024 (includes major tech rallies)

### Stage 2: Stress Test
- **Period**: 2024-02-01 to 2024-06-30 (5 months)
- **Time**: ~25-30 minutes
- **Threshold**: Drawdown < 45%
- **Purpose**: Test survival during the hardest market conditions
- **What it covers**: 2024 H1 — historically the worst "meat grinder" period for options strategies

### Stage 3: Medium
- **Period**: 2024-01-01 to 2025-06-30 (18 months)
- **Time**: ~45-60 minutes
- **Threshold**: Drawdown < 42%
- **Purpose**: Validate across bull/bear transitions and seasonal effects
- **What it covers**: Full 2024 volatility + 2025 early recovery

### Stage 4: Full Period
- **Period**: 2023-01-01 to 2026-01-31 (3 years)
- **Time**: ~2-3 hours
- **Threshold**: Drawdown < 40%, Sharpe >= 2.0, Profit >= 300%
- **Purpose**: Final acceptance test — benchmark against proven strategies
- **What it covers**: Complete market cycle including 2023 AI rally, 2024 correction, 2025 recovery

## Usage

### Configure windows

Define your validation windows in config:

```python
BACKTEST_WINDOWS = {
    "smoke_test": {
        "start": "2024-01-01",
        "end": "2024-03-31",
        "max_dd": 0.50,
        "expected_time": "15-20 min",
        "purpose": "Eliminate garbage fast",
    },
    "stress_test": {
        "start": "2024-02-01",
        "end": "2024-06-30",
        "max_dd": 0.45,
        "expected_time": "25-30 min",
        "purpose": "Survive worst conditions",
    },
    "medium": {
        "start": "2024-01-01",
        "end": "2025-06-30",
        "max_dd": 0.42,
        "expected_time": "45-60 min",
        "purpose": "Bull/bear transition stability",
    },
    "full": {
        "start": "2023-01-01",
        "end": "2026-01-31",
        "max_dd": 0.40,
        "expected_time": "2-3 hours",
        "purpose": "Final benchmark acceptance",
    },
}
```

### Run each stage

> **Prerequisite**: This skill coordinates validation stages. Actual backtest submission
> is handled by the **backtest-poller** skill (`cli.py`). Ensure that skill is installed
> and available on your path before running these commands.

```bash
# Stage 1: Smoke
# (using backtest-poller skill's cli.py)
python3 ../backtest-poller/cli.py submit \
  --main-file strategy.py --name "M31_smoke"

# Check what to run next:
python3 validator.py next M31 strategy.py

# Record the result after smoke completes:
python3 validator.py record M31 smoke_test --status passed --drawdown 0.32 --sharpe 2.1

# Stage 2: Stress (only if smoke passed)
python3 ../backtest-poller/cli.py submit \
  --main-file strategy.py --name "M31_stress"

python3 validator.py record M31 stress_test --status passed --drawdown 0.38 --sharpe 2.0

# Stage 3: Medium (only if stress passed)
python3 ../backtest-poller/cli.py submit \
  --main-file strategy.py --name "M31_medium"

python3 validator.py record M31 medium --status passed --drawdown 0.35 --sharpe 2.3

# Stage 4: Full (only if medium passed)
python3 ../backtest-poller/cli.py submit \
  --main-file strategy.py --name "M31_full"

python3 validator.py record M31 full --status passed --drawdown 0.30 --sharpe 2.5 --profit 3.2
```

## Skip Rules

Not every change needs to start from Smoke:

| Change Type | Start From |
|-------------|------------|
| Entry logic changed | Smoke (Stage 1) |
| Structural change (position sizing, survival) | Smoke (Stage 1) |
| Profit management only | Medium (Stage 3) |
| Date/parameter tweak | Same stage as before |

## Early-Stop Integration

This skill works alongside the **backtest-poller** skill (a separate package). The
backtest-poller's early-stop feature monitors drawdown in real time and deletes the
backtest run if the threshold is exceeded after 20% progress — no need to wait for
full completion of a doomed run. This validator tracks which stages passed or failed
locally, so you always know where to resume.

**Dependency**: Install the `backtest-poller` skill to enable submit/early-stop
functionality. This validator does not submit backtests itself.

## Time Savings Example

Testing 5 strategy variants, 3 of which are bad:

| Approach | Time |
|----------|------|
| Full backtest only | 5 x 3h = **15 hours** |
| Progressive validation | 3 x 15min + 1 x 45min + 1 x 3h = **~4.5 hours** |

**Savings: ~70%** of compute time.

## Rules

- **Never skip stages without justification.** The skip rules table above defines the only valid exceptions. If entry logic or survival structure changed, you must start from Smoke.
- **A strategy must pass a stage before advancing.** Do not promote a strategy to the next stage if the current stage resulted in early-stop or failure.
- **Do not modify stage thresholds mid-validation.** Changing `max_dd` between stages invalidates the progressive guarantee. Decide thresholds before starting.
- **One strategy variant per validation run.** Do not change the strategy code between stages — the point is to validate the same code across increasingly demanding windows.
- **Record every result**, even failures. Use `python3 validator.py record <strategy> <stage> --status passed|failed` to persist outcomes. Unrecorded results break the `next` and `status` commands.
