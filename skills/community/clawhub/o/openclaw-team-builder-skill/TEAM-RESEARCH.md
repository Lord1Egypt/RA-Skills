# Research Lab — Autonomous Experiment Methodology

Adapted from Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) framework. The core idea: set up a measurable experiment, run it in a fixed time budget, keep improvements, discard failures, and loop forever.

This methodology is **not limited to ML training**. It applies to any domain with a measurable metric: trading strategies, image analysis pipelines, prompt engineering, configuration tuning, data processing, and more.

Source reference: `reference/autoresearch-master/program.md` and `reference/autoresearch-master/README.md`

## Core Principles

1. **Fixed time budget** — every experiment runs for exactly the same duration, making results directly comparable
2. **Single metric** — one number that defines success (lower is better or higher is better — pick one)
3. **Keep or discard** — if the metric improved, keep the change; if not, revert
4. **Simplicity bias** — a small improvement that adds ugly complexity is not worth it; removing code for equal results is a win
5. **Never stop** — the loop runs until manually interrupted; the agent is fully autonomous

## The Experiment Loop

```
LOOP FOREVER:
  1. Review current state (baseline metric, recent experiments)
  2. Propose a hypothesis — what change might improve the metric?
  3. Implement the change (modify only the in-scope file/config)
  4. Run the experiment (fixed time budget)
  5. Measure the result
  6. Decision:
     - IMPROVED → keep the change, advance
     - EQUAL/WORSE → revert, try something else
     - CRASHED → fix if trivial, skip if fundamental
  7. Log the result to the experiment ledger
  8. Repeat
```

## Experiment Ledger Format

Log every experiment in a TSV file:

```
id	metric	status	description
baseline	0.9979	keep	baseline measurement
exp-001	0.9932	keep	increased learning rate to 0.04
exp-002	1.0050	discard	switched to GeLU activation
exp-003	0.0000	crash	doubled model width (OOM)
```

Columns: experiment ID, metric value, status (keep/discard/crash), short description of what was tried.

## Applying to Trading Strategy Optimization

**Metric**: Net P&L over backtest period, or win rate, or Sharpe ratio
**In-scope**: Strategy parameters (entry/exit thresholds, stop-loss, take-profit, indicator settings)
**Fixed budget**: 5-minute backtest window per experiment
**Ledger**: Track each parameter combination and its backtest result

```
LOOP:
  1. Read current strategy config from IG dashboard
  2. Propose parameter change (e.g., adjust RSI threshold from 30→25)
  3. Run backtest with modified parameters
  4. Compare P&L / win rate to baseline
  5. Keep if improved, revert if not
  6. Log to experiment ledger
```

### Integration with IG Agent
- IG agent provides market data and current strategy parameters
- Research loop modifies one parameter at a time (or small combinations)
- Backtest results come from the scalper engine or historical data
- Winning configurations get promoted to live via the Config Write API

## Applying to Image Analysis

**Metric**: Detection accuracy, classification confidence, or feature count
**In-scope**: Analysis parameters (thresholds, filters, model settings)
**Fixed budget**: Time per analysis run
**Ledger**: Track each configuration and its quality score

```
LOOP:
  1. Load image or image set
  2. Apply current analysis pipeline
  3. Measure quality metric (accuracy, features detected, etc.)
  4. Modify pipeline parameters
  5. Re-run and compare
  6. Keep improvements, discard regressions
```

### Integration with Artist Agent
- Artist provides image generation or acquisition
- Research loop iterates on analysis parameters
- Results feed back to Artist for enhanced generation prompts
- Applicable to: astronomy (star detection), medical imaging, satellite imagery, chart pattern recognition

## Applying to Prompt Engineering

**Metric**: Output quality score (human rating, automated evaluation, or downstream task performance)
**In-scope**: Prompt structure, wording, examples, system instructions
**Fixed budget**: N generations per prompt variant
**Ledger**: Track each prompt variant and its quality score

```
LOOP:
  1. Current prompt baseline
  2. Modify prompt (add detail, restructure, change examples)
  3. Generate N outputs with new prompt
  4. Score outputs against quality criteria
  5. Keep if average score improved
  6. Log variant and score
```

### Integration with Image Prompt Engineer
- Image Prompt Engineer proposes structured prompt variations
- Artist generates images for each variant
- Quality scored on technical accuracy, aesthetic appeal, brand alignment
- Best prompts advance, worst are discarded

## Constraints

- **Only modify the in-scope target** — do not change the measurement infrastructure, the evaluation metric, or the fixed constants
- **No new dependencies** — work within the existing toolset
- **Log everything** — every experiment gets recorded, even crashes
- **Simplicity criterion** — all else being equal, simpler is better
- **Timeout handling** — if an experiment exceeds 2x the time budget, kill it and log as crash

## Combining with Agency Specialists

Research loops benefit from domain experts:

| Domain | Research Role | Agency Specialist |
|--------|--------------|-------------------|
| Trading strategy | Parameter optimization | AI Engineer (model tuning) |
| UI performance | Load time optimization | Performance Benchmarker (measurement) |
| Image quality | Generation parameter tuning | Image Prompt Engineer (prompt structure) |
| API efficiency | Response time optimization | API Tester (validation) |
| Content quality | Prompt refinement | Content Creator (evaluation criteria) |
| Architecture | Config optimization | Backend Architect (system constraints) |

The Research Lab provides the experiment loop; the specialist provides domain expertise and evaluation criteria.
