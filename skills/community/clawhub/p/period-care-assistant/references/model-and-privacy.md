# Forecast Model And Privacy

## Storage Model

The helper script stores one encrypted JSON document containing:

- `version`
- `users.<userKey>.settings`
- `users.<userKey>.records[]`
- `users.<userKey>.reminder`

Encryption uses AES-256-GCM with a per-save random salt and IV. The data key is derived from `PERIOD_TRACKER_KEY` with `scrypt`.

## Forecast Method

The script predicts the next start date from recorded period start dates only. It does not infer end dates unless the user configures an estimated period length.

For cycle intervals, the script:

1. sorts unique start dates,
2. computes interval lengths between consecutive starts,
3. looks at the most recent six intervals,
4. blends median, weighted recent mean, and arithmetic mean,
5. clamps the result to a sensible 18-45 day range,
6. estimates confidence from recent variability and rolling historical error.

Why this model:

- median resists outliers,
- weighted mean adapts to recent trend changes,
- average smooths noise.

## Confidence

The script reports:

- `high`: enough samples and recent rolling mean absolute error is within roughly two days,
- `medium`: usable data but more variance,
- `low`: sparse or irregular history.

If the confidence is not high, avoid claiming the forecast satisfies a strict `±2` day target.

## Current Phase

The phase label is heuristic, based on:

- last recorded start date,
- estimated period length,
- expected ovulation window around `predictedCycleLength - 14`,
- reminder window before the next expected start.

These labels are for convenience only and should not be presented as medical advice.

## Delivery Reliability Caveat

No messaging stack can honestly guarantee absolute `100%` delivery across external providers. The best practical design is:

1. deterministic cron scheduling,
2. a stable per-user delivery route,
3. failure logging,
4. retry or escalation outside the skill if the provider reports failure.

This skill prepares the deterministic part. Transport guarantees depend on the configured OpenClaw channel or external DingTalk bridge.
