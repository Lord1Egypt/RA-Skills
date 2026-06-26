---
name: Prediction
slug: prediction
version: 1.0.0
homepage: https://clawic.com/skills/prediction
description: Forecast uncertain outcomes with base rates, reference classes, calibration loops, and explicit scorekeeping.
changelog: Initial release with question design, calibration, forecast review, and post-mortem workflows for probabilistic forecasting.
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/prediction/"]}}
---

## When to Use

User needs a defended forecast about what will happen, when it will happen, or how likely it is. Agent handles question design, base-rate search, reference-class selection, inside-vs-outside view balancing, explicit probability assignment, and after-action scoring.

Use it for business, product, technical, operational, policy, sports, market, or personal planning questions whenever the task is to forecast an uncertain outcome rather than just explain the present.

## Architecture

Memory lives in `~/prediction/`. If `~/prediction/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/prediction/
├── memory.md             # Activation rules, forecasting defaults, and durable lessons
├── forecast-log.md       # Open forecasts with probability, horizon, and next review date
├── scorecard.md          # Resolved forecasts, Brier scores, and error patterns
├── reference-classes.md  # Reusable base-rate cases by domain
├── assumptions.md        # Active drivers, fragilities, and update triggers
└── archive/              # Old resolved periods and retired forecasting themes
```

## Quick Reference

Use the smallest file that resolves the blocker.

| Topic | File | Use it for |
|-------|------|------------|
| First-run activation | `setup.md` | Integration behavior, storage boundaries, and first local state |
| Memory baseline | `memory-template.md` | Local templates for forecasts, scorecards, and assumptions |
| BRACE forecast loop | `forecast-loop.md` | End-to-end process from question intake to review |
| Forecastable question design | `question-design.md` | Turn vague prompts into resolvable prediction targets |
| Calibration and confidence | `calibration.md` | Map evidence quality into probabilities and abstention rules |
| Scoring and post-mortems | `scoring-and-review.md` | Score forecasts, inspect misses, and improve hit rate over time |

## Requirements

- No credentials or external services are required by default.
- Ask before storing sensitive personal forecasts, legal matters, health outcomes, or unreleased company information.
- Prefer questions with a clear resolution rule and time horizon. If those are missing, define them before assigning a probability.

## Prediction Contract

Every serious forecast should leave behind:

1. the exact question being forecast
2. the resolution rule and deadline
3. the base rate or reference class used
4. the main drivers that could move the answer
5. a numeric probability or ranked scenario split
6. the trigger that would cause an update before resolution
7. a later score or post-mortem once reality is known

This is the minimum needed to improve accuracy instead of producing forgettable guesses.

## Core Rules

### 1. Turn the Prompt Into a Resolvable Question First
- Use `question-design.md` before making any forecast that matters.
- If the target, threshold, deadline, or resolution source is fuzzy, the forecast is not auditable and the hit rate cannot improve.

### 2. Start With the Outside View Before the Story
- Pull a base rate or nearest reference class before building an inside-view narrative.
- Humans overweight unique details and underweight how often similar situations actually happen.

### 3. Run the BRACE Forecast Loop on Every Non-Trivial Prediction
- Use `forecast-loop.md`: Base rate, Resolution rule, Arguments both ways, Confidence assignment, Evaluation plan.
- A loop beats intuition because it forces evidence on both sides and leaves a trail for later scoring.

### 4. Express Uncertainty Numerically and Defend It
- Give a number, range, or explicit scenario split rather than words like "probably" or "maybe."
- Use `calibration.md` to map evidence quality, sample size, and model disagreement into probability levels.

### 5. Separate Signal From Narrative Heat
- Track what is actually predictive, what is merely interesting, and what is just recent or vivid.
- Strong stories with weak base rates are noise, not edge.

### 6. Update Only on Information That Changes the Odds
- Pre-commit to update triggers: deadline changes, threshold changes, a major driver flips, or new data changes the reference class.
- Constant micro-updating on every headline produces churn without better accuracy.

### 7. Score Every Meaningful Forecast and Learn From Misses
- Use `scoring-and-review.md` after resolution and store the result in the local scorecard.
- Unscored forecasts feel smart in the moment and teach nothing later.

## Common Traps

These are the failure modes that usually destroy forecast accuracy even when the reasoning sounds smart.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Predicting a vibe instead of an event | The forecast cannot be scored or falsified | Rewrite into one resolvable question with a deadline |
| Going straight to inside-view storytelling | Unique details swamp the real base rate | Start with the nearest reference class and only then adjust |
| Using words instead of numbers | "Likely" means different things to different people | Give a probability, range, or scenario table |
| Refusing to abstain | Forced certainty creates fake precision | Say what is missing and hold a low-confidence or no-call position |
| Treating new information as equally important | Noise looks like signal | Update only when a driver or resolution rule actually changes |
| Forgetting to track misses | Accuracy never compounds | Score the forecast, log the error type, and update the reference class |
| Confusing decision advice with certainty | A good decision can still have a bad outcome | Keep probability, recommendation, and risk management separate |

## Data Storage

Local state in `~/prediction/` may include:
- activation preferences and forecasting defaults
- open forecasts with probabilities, scenarios, and review dates
- resolved forecasts with scores and miss patterns
- reusable reference classes and base-rate notes
- assumptions and update triggers for active forecasting topics

Store only the smallest durable note that improves the next forecast.

## Security & Privacy

**Data that stays local:**
- forecast logs, scorecards, assumptions, and reference-class notes in `~/prediction/`

**Data that leaves your machine:**
- none by default unless the current environment uses approved search or browsing tools for evidence collection

**This skill does NOT:**
- claim certainty where evidence is weak
- guarantee accuracy or positive expected value
- place bets, trades, or automatic decisions on the user's behalf
- store credentials, account numbers, or private medical records
- modify its own skill file

## Scope

This skill ONLY:
- turns ambiguous prediction prompts into auditable forecasting questions
- uses base rates, reference classes, and explicit probability assignments
- tracks forecast quality through scoring and post-mortems
- stores lightweight local notes that improve later predictions

This skill NEVER:
- pretend that every question is forecastable with confidence
- replace licensed legal, medical, or investment advice
- confuse eloquent explanation with predictive power
- skip scoring on forecasts that matter

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `analysis` - structure assumptions, causal chains, and trade-offs before forecasting.
- `compare` - evaluate scenario branches and option differences after the forecast is framed.
- `decide` - turn probabilities and uncertainty into explicit decision choices.
- `statistics` - dig deeper into inference, distributions, and sampling logic behind the forecast.

## Feedback

- If useful: `clawhub star prediction`
- Stay updated: `clawhub sync`
