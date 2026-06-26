# Setup - Prediction

Use this file when `~/prediction/` is missing or empty, or when the user wants forecasting to become a recurring capability.

Answer the immediate prediction question first, then lock activation behavior early so future forecasting work starts with the right level of rigor instead of guessing from scratch.

## Immediate First-Run Actions

### 1. Lock integration behavior early

Within the first exchanges, clarify:
- should this activate whenever the user asks what is likely, what will happen, or what odds to assign
- should it jump in proactively for uncertain plans and bets, or only on explicit request
- whether rough estimation questions should route here, `analysis`, or `decide`

Keep this short. One clear routing answer is enough.

### 2. Learn the user's forecasting style

Understand the defaults that change prediction quality:
- domains they forecast most: business, product, engineering, markets, sports, politics, life planning, or mixed
- what output helps most: single-number probability, scenario ranges, confidence bands, or decision memo
- how aggressive they want updates to be: only on major evidence or after any material signal
- whether they care more about hit rate, calibration, downside avoidance, or speed

Start broad, then narrow only where the current prediction needs it.

### 3. Lock boundaries and storage scope

Clarify:
- what should be remembered across forecasts: preferred probability format, favored domains, known blind spots, update cadence, scoring habits
- what should stay out of memory: secrets, account details, health records, legal case specifics, or unreleased sensitive information
- whether examples may be stored in shorthand form or should stay fully ephemeral

### 4. Create local state after the routing contract is clear

```bash
mkdir -p ~/prediction/archive
touch ~/prediction/memory.md
touch ~/prediction/forecast-log.md
touch ~/prediction/scorecard.md
touch ~/prediction/reference-classes.md
touch ~/prediction/assumptions.md
chmod 700 ~/prediction ~/prediction/archive
chmod 600 ~/prediction/memory.md ~/prediction/forecast-log.md ~/prediction/scorecard.md ~/prediction/reference-classes.md ~/prediction/assumptions.md
```

If the files are empty, initialize them from `memory-template.md`.

### 5. What to save

Save only what improves the next forecast:
- activation behavior and routing preferences
- recurring domains, default probability style, and update preferences
- open forecasts that need revisiting
- resolved forecasts with scores and miss patterns
- reference classes and assumptions that recur often enough to matter

Do not store secrets, financial credentials, health details, or private case files.
