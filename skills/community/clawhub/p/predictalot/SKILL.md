---
name: predictalot
description: Self-hosted forecasting/prediction service. Foundation time-series endpoints under /v1/timeseries/<type>/{forecast,forecast/ensemble} + GET .../models — univariate, past/future/both covariates, multivariate, samples — over 5 zero-shot models (chronos-2, timesfm-2.5, moirai-2, toto-1, sundial-base-128m). Plus supervised tabular ML under /v1/tabular/ (9 backends — lightgbm, xgboost, hist-gbt, random-forest, logistic, mlp, svm-rbf, knn, naive-bayes — over direction/value/quantile modes) with train+persist, weighted ensembles, and calibrated/stacking/diversified meta-learners. Unified REST + MCP (streamable-HTTP at /mcp, one tool per (type, model) cell + per-type ensemble + listing) + optional bearer auth. Use when the user wants to forecast a numeric time series (quantile bands or raw sample paths), condition a forecast on known/future covariates, ensemble several forecasters, or train a tabular model on engineered features and predict direction/value/quantiles on the latest snapshot.
homepage: https://github.com/psyb0t/docker-predictalot
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🔮", "primaryEnv": "PREDICTALOT_URL", "requires": { "bins": ["docker", "curl"] } } }
permissions:
  network: "outbound HTTP(S) to the configured PREDICTALOT_URL only (forecast/train/model-management calls + MCP at /mcp)"
  shell: "docker + curl invocations shown in setup.md and this file (container lifecycle, request examples) — no other host access"
---

# predictalot

Self-hosted forecasting service — one HTTP container, two model families.

- **Foundation time-series (zero-shot)** — 5 forecasters (`chronos-2`, `timesfm-2.5`, `moirai-2`, `toto-1`, `sundial-base-128m`). Hand them a context window, get quantile bands or raw sample paths. No training step. Routed by forecast type under `/v1/timeseries/<type>/` — `univariate`, `covariates/past`, `covariates/future`, `covariates` (past+future), `multivariate`, `samples`. Each type has `forecast`, `forecast/ensemble`, and a `models` listing.
- **Tabular ML (supervised)** — 9 learners (`lightgbm`, `xgboost`, `hist-gbt`, `random-forest`, `logistic`, `mlp`, `svm-rbf`, `knn`, `naive-bayes`), all supporting 3 modes (`direction` / `value` / `quantile`). Train on YOUR engineered features, persist server-side by `modelId`, forecast on the latest feature snapshot. Weighted ensembles over stored models plus 3 meta-learners (`calibrated` / `stacking` / `diversified`). Under `/v1/tabular/`.
- **MCP** — streamable-HTTP tools at `/mcp`. One tool per (FM type, model) cell plus per-type ensemble + listing. Tabular is HTTP-only.
- **Model lifecycle** — `POST /v1/models/unload` releases every resident foundation model. A forecast's `unload: true` waits for concurrent forecasts using that model, then tears it down. The MCP equivalent is `unload_models`.
- **Auth** — optional bearer token (`PREDICTALOT_AUTH_TOKENS` on the server; refuses to start with no tokens unless `PREDICTALOT_ALLOW_NO_AUTH=1`).

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **Network-exposed** — predictalot is a plain HTTP + MCP service; anyone who can reach the port can call it. Set `PREDICTALOT_AUTH_TOKENS` to a strong generated secret (`$(openssl rand -hex 32)`) and bind to loopback (`-p 127.0.0.1:8080:8080`) by default. Only expose beyond loopback behind a reverse proxy / VPN, and never with the default/example token.
- **External transmission** — every forecast/train call sends your time series, engineered feature values, and/or `modelId`s to whatever `PREDICTALOT_URL` points at — that data leaves your host. Point it only at a service you run or explicitly trust; prefer HTTPS.
- **Consumer-only** — this skill talks to an instance you already run and trusts. It never provisions, starts, or hardens the server; that's the operator's job (see setup.md).
- **Destructive delete requires confirmation** — `DELETE /v1/tabular/models/{modelId}` permanently removes a trained model and cannot be undone. Only call it against a `modelId` you obtained from a prior `GET /v1/tabular/models` (or a train response) in this session, and get explicit user confirmation before issuing the delete.

## When To Use

- Forecast a numeric time series N steps ahead and get calibrated quantile bands (`0.1`/`0.5`/`0.9`, etc.) — zero-shot, no training.
- Get raw Monte-Carlo sample paths (via the `samples` type) to compute custom risk metrics / joint distributions across horizon steps.
- Condition a forecast on covariates: known-history (`covariates/past`), forward-known drivers like a planned promotion or price schedule (`covariates/future`), or both at once (`covariates`).
- Forecast several correlated channels jointly (`multivariate`).
- Combine multiple forecasters into a weighted ensemble and inspect each member's individual forecast + applied weight.
- Train a supervised model on engineered features and predict next-bar direction (`P(up)`), a point value, or quantiles on the latest snapshot.
- Combine trained tabular models via ensemble or a `calibrated` / `stacking` / `diversified` meta-learner.

## When NOT To Use

- Real-time / streaming forecasts — every endpoint is request/response only.
- Automatic feature engineering on the tabular side — you supply the features; predictalot does not derive indicators or lags for you.
- `timesfm-2.5` for accuracy — it is the weakest of the five on every benchmarked dataset. Skip it or set `weights={"timesfm-2.5": 0}` in ensembles.
- Commercial use of `moirai-2` — it ships under CC-BY-NC-4.0 (non-commercial). The other four FMs are Apache 2.0.
- Covariate/multivariate/samples types on models that don't support them — membership is fixed per type (see below). A non-member `model` → 400.
- Provisioning or hardening the server from here — this skill is a **consumer**. It talks to an instance the user already runs and trusts; it never launches, escalates, or reconfigures the container.

## Setup

The container should already be running. Point at it:

```bash
export PREDICTALOT_URL=http://localhost:8080
```

If the server has `PREDICTALOT_AUTH_TOKENS` set, export a token too:

```bash
export PREDICTALOT_AUTH_TOKEN=<your-token>
# every /v1/* and /mcp request below needs: -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN"
```

**Verify:** `curl $PREDICTALOT_URL/healthz` returns `{"ok": true}`. (`/healthz` is unauthenticated.)

For install / configuration / env vars / CPU vs CUDA images, see [references/setup.md](references/setup.md).

## Models & Types

Foundation models, and which forecast types each supports (a `model` outside a type's member set → 400):

| Model | Univariate | Multivariate | Cov: past | Cov: future | Cov: both | Samples | License | Recommended for |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| `chronos-2` | ✓ | ✓ | ✓ | ✓ | ✓ | — | Apache 2.0 | Default all-rounder; fastest on CPU; only model with future/both covariates. |
| `timesfm-2.5` | ✓ | — | — | — | — | — | Apache 2.0 | Weakest on benchmarks — skip or zero-weight it. Univariate-only; compile-time horizon cap. |
| `moirai-2` | ✓ | ✓ | ✓ | — | — | — | CC-BY-NC-4.0 | Clean cyclic/seasonal series; correlated channels. Non-commercial license. |
| `toto-1` | ✓ | ✓ | — | — | — | ✓ | Apache 2.0 | Noisy / observability / financial series; exposes raw sample paths. |
| `sundial-base-128m` | ✓ | — | — | — | — | ✓ | Apache 2.0 | Drifting / trending series; generative sample paths. Runs in a sidecar venv. |

Type → URL prefix:

| Type | URL prefix | Members |
|---|---|---|
| univariate | `/v1/timeseries/univariate` | chronos-2, timesfm-2.5, moirai-2, toto-1, sundial-base-128m |
| multivariate | `/v1/timeseries/multivariate` | chronos-2, moirai-2, toto-1 |
| covariates (past) | `/v1/timeseries/covariates/past` | chronos-2, moirai-2 |
| covariates (future) | `/v1/timeseries/covariates/future` | chronos-2 |
| covariates (past+future) | `/v1/timeseries/covariates` | chronos-2 |
| samples | `/v1/timeseries/samples` | toto-1, sundial-base-128m |

Discover live per-type membership + runtime state with `GET /v1/timeseries/<type>/models`. Discover tabular backends with `GET /v1/tabular/backends`.

Tabular backends (all support `direction` / `value` / `quantile`):

| Slug | Display name | Category |
|---|---|---|
| `lightgbm` | LightGBM | boosting |
| `xgboost` | XGBoost | boosting |
| `hist-gbt` | HistGradientBoosting (sklearn) | boosting |
| `random-forest` | Random Forest | bagging |
| `logistic` | Logistic / Ridge / QuantileRegressor (linear baselines) | linear |
| `mlp` | Multi-Layer Perceptron (sklearn) | neural |
| `svm-rbf` | SVM with RBF kernel | kernel |
| `knn` | k-Nearest Neighbors | distance |
| `naive-bayes` | Gaussian Naive Bayes / BayesianRidge | independence |

## Quick Start

> Every forecast/train call below sends your time series, engineered features, and/or `modelId`s over the network to `$PREDICTALOT_URL`. Only point this at a trusted, self-hosted instance you control, prefer HTTPS, treat proprietary datasets as sensitive, and never echo `PREDICTALOT_AUTH_TOKEN` in output.

```bash
# Health (unauthenticated).
curl -s $PREDICTALOT_URL/healthz | jq

# List univariate models + their runtime state.
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/models \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq

# Zero-shot univariate forecast: 5 steps ahead of one series, chronos-2.
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/forecast \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "chronos-2",
        "context": [[10,11,12,13,14,15,16,17,18,19,20]],
        "config": { "horizon": 5, "quantileLevels": [0.1, 0.5, 0.9] }
      }' | jq
```

Wire format is **camelCase** (`quantileLevels`, `contextLength`, `pastCovariates`, `futureCovariates`, `numSamples`, `memberOverrides`, `modelId`). All `/v1/*` routes require the bearer header when the server has tokens configured; drop the header for an open-auth deployment.

Shapes recur across the timeseries API: `context` is `[series][time]` (a batch of independent series), `horizon` > 0, `quantileLevels` is a subset of `{0.1, 0.2, …, 0.9}` (default `[0.1, 0.5, 0.9]`), `contextLength` caps history fed to the model (omit → per-model default), `unload: true` tears the model down after the response. `median` and `quantiles["0.5"]` are the same for most models but can differ for chronos-2 (its `median` is the distribution mean).

Release every resident foundation model when the next task will not need one:

```bash
curl -s -X POST $PREDICTALOT_URL/v1/models/unload \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq
```

The request returns `409` while a foundation forecast is active. Do not retry it blindly. Wait for the forecast result, then retry when memory needs to be freed.

---

## API — `POST /v1/timeseries/univariate/forecast`

Single-model quantile forecast over a batch of independent series. `context` (your time series data) transmits off-box to `$PREDICTALOT_URL` — same data-transfer note as Quick Start applies to every timeseries endpoint below.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `model` | yes | — | One of the univariate members. Not a member → 400; unknown slug → 404. |
| `context` | yes | — | `[series][time]` — one inner list of floats per series. |
| `config.horizon` | yes | — | Steps ahead. Must be `> 0` (else 422). |
| `config.quantileLevels` | no | `[0.1, 0.5, 0.9]` | Subset of `{0.1..0.9}` step 0.1. Out-of-range → 400. |
| `config.contextLength` | no | per-model | Max history points fed to the model. `> 0`. |
| `config.extra` | no | — | Per-backend escape-hatch dict, camelCased. Unknown keys ignored. E.g. chronos-2: `batchSize`, `crossLearning`, `limitPredictionLength`; toto-1: `numSamples`, `samplesPerBatch`, `useKvCache`; timesfm-2.5: `normalizeInputs`, `fixQuantileCrossing`, … |
| `unload` | no | `false` | Unload the model after responding. |

### Response

```json
{
  "model": "chronos-2",
  "horizon": 5,
  "quantileLevels": [0.1, 0.5, 0.9],
  "median": [[20.9, 21.8, 22.7, 23.6, 24.5]],
  "quantiles": {
    "0.1": [[20.1, 20.8, 21.5, 22.1, 22.7]],
    "0.5": [[20.9, 21.8, 22.7, 23.6, 24.5]],
    "0.9": [[21.7, 22.9, 24.0, 25.1, 26.3]]
  }
}
```

`median` is `[series][time]`; `quantiles` maps each level string → `[series][time]`.

### Error Contract

| Status | Shape | When |
|---|---|---|
| 200 | forecast JSON | success |
| 400 | `{"detail": "..."}` | empty context/series, model not a member of the type, quantile level outside `{0.1..0.9}`, horizon over a model's compile-time cap (timesfm-2.5 / moirai-2) |
| 401 | `{"detail": "..."}` | tokens configured, missing/wrong bearer |
| 404 | `{"detail": "..."}` | unknown `model` slug |
| 413 | `{"detail": "..."}` | body over `PREDICTALOT_MAX_BODY_SIZE` |
| 422 | `{"detail": [...]}` | Pydantic validation (missing/typed fields, `horizon` not `> 0`) |
| 503 | `{"detail": "..."}` | snapshot download failed, inference threw, or sundial sidecar unreachable |

---

## API — `POST /v1/timeseries/univariate/forecast/ensemble`

Weighted mean across every univariate member. No `model` field — membership is the whole type.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `context` | yes | — | `[series][time]`. |
| `config` | yes | — | Same `ForecastConfig` as single forecast (`horizon`, `quantileLevels`, `contextLength`, `extra`). |
| `weights` | no | uniform | `{slug: float ≥ 0}`. Missing slugs default to 1.0; weight `0` disables a member; unknown slug → 400. |
| `memberOverrides` | no | — | `{slug: partial-config}` — per-member overrides of the global `config` (e.g. give one member a different `contextLength` or `extra`). |
| `unload` | no | `false` | Unload members after responding. |

### Response

Aggregated `median` + `quantiles` (same shapes as single forecast) with `model: "ensemble"`, plus:

```json
{
  "model": "ensemble",
  "horizon": 5,
  "quantileLevels": [0.1, 0.5, 0.9],
  "median": [[...]],
  "quantiles": { "0.1": [[...]], "0.5": [[...]], "0.9": [[...]] },
  "ensembleMembers": ["chronos-2", "moirai-2", "toto-1"],
  "weights": { "chronos-2": 0.5, "moirai-2": 0.25, "toto-1": 0.25 },
  "individual": {
    "chronos-2": { "model": "chronos-2", "horizon": 5, "quantileLevels": [...],
                   "median": [[...]], "quantiles": {...}, "weight": 0.5 }
  }
}
```

`individual[slug]` is that member's full single-forecast response + its applied `weight`.

### Error Contract

Same as single univariate, minus 404 (no `model` field) — an unknown `weights` slug is a 400, not 404.

---

## API — `POST /v1/timeseries/covariates/past/forecast`

Forecast each target series conditioned on covariates known only up to `t`. Members: `chronos-2`, `moirai-2`.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `model` | yes | — | A past-covariate member. |
| `context` | yes | — | `[series][time]` — the univariate targets. |
| `pastCovariates` | yes | — | `list[dict[name, float[]]]` — one mapping per series; every value array is the **same length as that series' context**. All series share the same covariate names. |
| `config` | yes | — | `ForecastConfig` (`horizon`, `quantileLevels`, `contextLength`, `extra`). |
| `unload` | no | `false` | |

### Response

Identical shape to univariate single forecast (`model`, `horizon`, `quantileLevels`, `median`, `quantiles`).

### Error Contract

Same table as univariate, plus 400 when a `pastCovariates` value length doesn't match the matching `context` series.

---

## API — `POST /v1/timeseries/covariates/past/forecast/ensemble`

Weighted ensemble over the past-covariate members. Fields = past forecast fields plus `weights` + `memberOverrides` (as in the univariate ensemble). Response = univariate ensemble shape.

---

## API — `POST /v1/timeseries/covariates/future/forecast`

Forecast conditioned on covariates known only over the **future window** (length == `horizon`) — e.g. a planned promotion, a published price schedule, a weather forecast. Member: `chronos-2` only.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `model` | yes | — | `chronos-2`. |
| `context` | yes | — | `[series][time]` targets. |
| `futureCovariates` | yes | — | `list[dict[name, float[]]]` — one mapping per series; **each value array of length `horizon`**. All series share names. |
| `config` | yes | — | `ForecastConfig`. |
| `unload` | no | `false` | |

### Response

Univariate single-forecast shape.

### Error Contract

Univariate table + 400 when a `futureCovariates` value length ≠ `config.horizon`.

---

## API — `POST /v1/timeseries/covariates/future/forecast/ensemble`

Ensemble over future-covariate members (currently just `chronos-2`, so only useful once more back it). Fields = future forecast + `weights` + `memberOverrides`. Response = univariate ensemble shape.

---

## API — `POST /v1/timeseries/covariates/forecast` (past + future)

Combined past **and** future covariates in one call. Member: `chronos-2` only.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `model` | yes | — | `chronos-2`. |
| `context` | yes | — | `[series][time]` targets. |
| `pastCovariates` | yes | — | Per series, same length as context. |
| `futureCovariates` | yes | — | Per series, length `horizon`. **Every future-covariate name MUST also appear in `pastCovariates`** for that series (chronos-2 constraint) — else 400. |
| `config` | yes | — | `ForecastConfig`. |
| `unload` | no | `false` | |

### Response

Univariate single-forecast shape.

### Error Contract

Univariate table + 400 for length mismatches or a future-covariate name missing from `pastCovariates`.

---

## API — `POST /v1/timeseries/covariates/forecast/ensemble`

Ensemble over past+future members. Fields = past+future forecast + `weights` + `memberOverrides`. Response = univariate ensemble shape.

---

## API — `GET /v1/timeseries/<type>/models`

Per-type model listing + runtime state. `<type>` ∈ `univariate`, `multivariate`, `covariates/past`, `covariates/future`, `covariates`, `samples`.

### Response

```json
{
  "type": "univariate",
  "models": [
    { "slug": "chronos-2", "loaded": true, "lastUsedSecsAgo": 12.4, "idleTimeoutSecs": 1800.0 },
    { "slug": "timesfm-2.5", "loaded": false, "lastUsedSecsAgo": null, "idleTimeoutSecs": 1800.0 }
  ]
}
```

`lastUsedSecsAgo` is `null` when the model has never loaded. `idleTimeoutSecs` reflects `PREDICTALOT_MODEL_IDLE_TIMEOUT` (or a per-slug override); `0` means never auto-unloaded.

### Error Contract

200 on success; 401 when tokens are configured and the bearer is missing/wrong.

---

## API — `GET /v1/tabular/backends`

List the supervised tabular backends and the modes each supports. Use this to discover the live set before a train call.

### Response

```json
{
  "backends": [
    { "slug": "lightgbm", "displayName": "LightGBM", "category": "boosting",
      "supportedModes": ["direction", "quantile", "value"] },
    { "slug": "xgboost", "displayName": "XGBoost", "category": "boosting",
      "supportedModes": ["direction", "quantile", "value"] }
  ]
}
```

### Error Contract

200 on success; 401 when tokens are configured and the bearer is missing/wrong.

---

## Tabular API (train → forecast)

The tabular side trains on YOUR engineered features and persists a model server-side by `modelId`. `target` / `features` are generic float lists — no OHLC / indicator assumptions. `features` is per series: `featureName → time-aligned float list`. Same data-transfer note as Quick Start applies: `target`/`features`/`modelId` all transmit to `$PREDICTALOT_URL`.

### `POST /v1/tabular/train`

| Field | Required | Default | Notes |
|---|---|---|---|
| `modelId` | yes | — | Caller-chosen id, used for storage + later forecast lookup. |
| `backend` | yes | — | A slug from `GET /v1/tabular/backends`. Unknown → 404. |
| `target` | yes | — | `[series][time]` — the scalar series to predict. Empty → 400. |
| `features` | yes | — | `list[dict[name, float[]]]` — same length + names per series as `target`. Count must match `target` (else 400); differing key sets across series → 400. |
| `config.mode` | yes | — | `direction` (sign of `target[t+h] - target[t]`) / `value` (regress `target[t+h]`) / `quantile`. Mode not supported by the backend → 400. |
| `config.horizon` | yes | — | Bars ahead (`t+h`). `> 0`. |
| `config.quantileLevels` | when `quantile` | — | Required for `mode="quantile"`; subset of `{0.1..0.9}`. |
| `config.*` (tier-2) | no | — | `nEstimators`, `maxDepth`, `learningRate`, `numLeaves`, `minSamples`, `randomState`, `categoricalFeatures`, `monotonicConstraints`, `classWeight`, `sampleWeight`, `earlyStoppingRounds`, `validationFraction`. Backends ignore knobs they don't use. |
| `config.extra` | no | — | Per-backend hyperparams (e.g. svm-rbf reads `C`/`gamma`; mlp reads `hiddenLayerSizes`/`activation`; knn reads `nNeighbors`/`weights`/`metric`). |
| `overwrite` | no | `false` | Reuse an existing `modelId` → 409 unless `true`. |

**Response** (`TrainResponse`): `modelId`, `backend`, `mode`, `horizon`, `nTrainingRows`, `nFeatures`, `featureNames`, `featureImportance` (`{name: float}`), `trainSecs`.

### `POST /v1/tabular/forecast`

Runs a stored model on the **latest** feature snapshot — the LAST row per series is the anchor; earlier rows are ignored.

| Field | Required | Notes |
|---|---|---|
| `modelId` | yes | Missing → 404. If its backend is no longer registered → 410. |
| `features` | yes | `list[dict[name, float[]]]`; names must match training. Missing a trained name → 400. |

**Response** (`ForecastResponse`) is mode-dependent:
- `direction`: `probUp: float[]` (per series) + `confidence: float[]` (`|probUp-0.5|*2`).
- `value`: `predicted: float[]`.
- `quantile`: `median: float[series][1]` + `quantiles: {level: float[series][1]}`.

### `POST /v1/tabular/forecast/ensemble`

Weighted combination of several stored models on the same features; all members must share `mode`, `horizon`, and `featureNames` (mismatch → 400).

| Field | Required | Notes |
|---|---|---|
| `modelIds` | yes | Stored ids to combine (≥ 1). Any missing → 404. |
| `weights` | no | `{modelId: float ≥ 0}`. None → uniform; `0` removes a member; unknown id or negative → 400. |
| `features` | yes | As in forecast; last row per series is the anchor. |

**Response** (`EnsembleForecastResponse`): `mode`, `horizon`, `ensembleMembers`, normalized `weights`, `individual` (`{modelId: member response}`), plus the combined mode-specific fields (`probUp`+`confidence` / `predicted` / `median`+`quantiles`).

### `GET /v1/tabular/models` and `DELETE /v1/tabular/models/{modelId}` (destructive)

`GET` lists stored models: `{"models": [{ modelId, backend, mode, horizon, nFeatures, featureNames, nTrainingRows, trainedAtUnix }]}`. `DELETE` removes one (`{"modelId": "...", "removed": true}`; 404 if absent) — **irreversible**. Only delete a `modelId` returned by a prior `GET /v1/tabular/models` call (or a train response), and get explicit user confirmation first.

### Meta-learners

Composite endpoints that hold out / cross-validate internally so you don't have to orchestrate it client-side. Each persists one blob under a `meta:<kind>` backend tag and forecasts via `POST /v1/tabular/forecast/<kind>` with `{modelId, features}`.

- `POST /v1/tabular/train/calibrated` — base learner + post-hoc probability calibrator. **`direction` only.** Fields: `modelId`, `baseBackend`, `target`, `features`, `config` (mode must be `direction`), `calibrationMethod` (`sigmoid`|`isotonic`, default `sigmoid`), `calibrationFraction` (default `0.2`, in `(0,1)`), `overwrite`. Too-small split → 400.
- `POST /v1/tabular/train/stacking` — K base learners + a meta-learner on K-fold OOF predictions. **`direction` only (v1).** Fields: `modelId`, `members` (≥ 2 `{backend, config}`, all `direction`, horizon == top-level), `metaBackend` (default `logistic`), `target`, `features`, `horizon`, `nFolds` (2–10, default 5), `overwrite`. Needs `≥ nFolds*5` rows. Response includes `oofScore` (AUC).
- `POST /v1/tabular/train/diversified` — trains K candidates, selects a low-correlation subset by OOF Pearson correlation, combines equal-weight. Supports all 3 modes. Fields: `modelId`, `candidates` (≥ 2, mode+horizon must match top-level), `target`, `features`, `horizon`, `mode`, `quantileLevels` (required if `quantile`), `nFolds` (2–10, default 3), `maxPairwiseCorr` (0–1, default 0.85), `minMembers`, `maxMembers`, `overwrite`. Response includes `candidateCorr`.

Meta-train responses (`MetaTrainResponse`): `modelId`, `kind`, `mode`, `horizon`, `membersUsed`, `nTrainingRows`, `nFeatures`, `featureNames`, `trainSecs`, plus `oofScore` (stacking) / `candidateCorr` (diversified). Meta-forecast responses (`MetaForecastResponse`): `modelId`, `kind`, `mode`, `horizon`, `members` (per-member breakdown), `selectedMembers` (diversified), and the mode-specific combined fields.

### Tabular Error Contract

| Status | When |
|---|---|
| 200 | success |
| 400 | empty `target`; `target`/`features` count mismatch; differing feature key sets; mode unsupported by backend; `quantile` without `quantileLevels`; forecast features missing a trained name; ensemble member mode/horizon/features mismatch; unknown/negative ensemble weight; meta constraint violated (calibrated non-direction, stacking non-direction, diversified quantile w/o levels, split too small) |
| 401 | tokens configured, missing/wrong bearer |
| 404 | unknown tabular `backend` on train; `modelId` not found on forecast/meta |
| 409 | train with `overwrite: false` against an existing `modelId` |
| 410 | forecast against a `modelId` whose backend is no longer registered |
| 413 | body over `PREDICTALOT_MAX_BODY_SIZE` |
| 422 | Pydantic validation |
| 503 | training/inference threw |

---

## MCP Endpoint (`/mcp`)

predictalot mounts a [Model Context Protocol](https://modelcontextprotocol.io) server over Streamable HTTP at `/mcp`, in the same process, behind the same bearer auth. The tool surface mirrors the **foundation-model** routes only — tabular is HTTP-only.

For each forecast type there are three classes of tool:
- `forecast_<type>_<model>` — single-model forecast for one (type, model) cell. Types are underscore-normalized: `univariate`, `multivariate`, `covariates_past`, `covariates_future`, `covariates_both`, `samples`; model slugs are underscore-normalized too (`chronos-2` → `chronos_2`). E.g. `forecast_univariate_chronos_2`, `forecast_covariates_future_chronos_2`.
- `forecast_<type>_ensemble` — weighted ensemble over every model supporting that type.
- `list_<type>_models` — which models implement the type + runtime state (`{type, models: [{slug, loaded, lastUsedSecsAgo, idleTimeoutSecs}]}`).

Tool args mirror the HTTP bodies but flattened (no nested `config`): `context`, `horizon`, `quantile_levels?`, `context_length?`, `unload?`; covariate tools add `past_covariates` / `future_covariates`; ensemble tools add `weights?`; samples tools use `num_samples?` instead of quantile levels and return `samples` `[series][sample][time]` + `median`.

Wire it into Claude Code (auth optional — the token may also be passed as `?apiToken=<token>`):

```bash
claude mcp add --transport http predictalot $PREDICTALOT_URL/mcp \
  --header "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN"
```

### Raw JSON-RPC

The transport requires `Accept: application/json, text/event-stream`.

```bash
# tools/list — enumerate every (type, model) tool + ensembles + listings.
curl -s $PREDICTALOT_URL/mcp/ \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# tools/call — univariate chronos-2 forecast.
curl -s $PREDICTALOT_URL/mcp/ \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
    "params": {
      "name": "forecast_univariate_chronos_2",
      "arguments": {
        "context": [[10,11,12,13,14,15,16,17,18,19,20]],
        "horizon": 5,
        "quantile_levels": [0.1, 0.5, 0.9]
      }
    }
  }'
```

Each tool returns a JSON-encoded string. User-input errors come back as `{"error": "...", "context": "<type>/<model>"}`; internal errors are redacted to `{"error": "internal error; see server logs", "context": "..."}`.

## Bearer-Token Auth

If `PREDICTALOT_AUTH_TOKENS` (comma-separated list) is set on the server, every `/v1/*` and `/mcp` request needs `Authorization: Bearer <one-of-the-tokens>`; `/healthz` is always open. Missing/wrong → 401. Tokens are compared constant-time (`hmac.compare_digest`).

```bash
export PREDICTALOT_AUTH_TOKEN=<your-token>
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/models \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq
```

The server **refuses to start** with an empty token list unless it was launched with `PREDICTALOT_ALLOW_NO_AUTH=1` — in that open-auth mode there is no 401 and no header is needed. For untrusted networks, combine the token with a reverse proxy doing TLS + rate limiting.

## Typical Workflows

### Pick a model → forecast → read the intervals

```bash
# 1. See which univariate models are available + resident.
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/models \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq -r '.models[].slug'

# 2. Forecast with chronos-2 (default all-rounder), 12 steps, three bands.
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/forecast \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"chronos-2","context":[[100,102,101,105,110,108,112,115,120,118,125,130]],
       "config":{"horizon":12,"quantileLevels":[0.1,0.5,0.9]}}' | jq

# 3. Read the interval: quantiles["0.5"] is the central path,
#    ["0.1"]/["0.9"] the 80% band — all shaped [series][time].
```

### Ensemble, zero-weighting the weak model

```bash
curl -s $PREDICTALOT_URL/v1/timeseries/univariate/forecast/ensemble \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"context":[[100,102,101,105,110,108,112,115,120,118,125,130]],
       "config":{"horizon":12},
       "weights":{"timesfm-2.5":0,"chronos-2":2,"toto-1":1}}' | jq \
  '{members: .ensembleMembers, weights, median}'
```

### Future-covariate forecast (chronos-2)

```bash
# Target has 8 steps of history; horizon 4 → futureCovariates arrays length 4.
curl -s $PREDICTALOT_URL/v1/timeseries/covariates/future/forecast \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"chronos-2",
       "context":[[20,22,21,25,24,27,29,31]],
       "futureCovariates":[{"promo":[0,1,1,0]}],
       "config":{"horizon":4}}' | jq
```

### Raw sample paths for custom risk metrics

```bash
curl -s $PREDICTALOT_URL/v1/timeseries/samples/forecast \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"toto-1",
       "context":[[100,102,101,105,110,108,112,115,120,118,125,130]],
       "config":{"horizon":10,"numSamples":256}}' | jq '{numSamples, shape: (.samples[0]|length)}'
# samples is [series][sample][time]; compute your own VaR / quantiles off the draws.
```

### Train a tabular direction model, then forecast the latest snapshot

```bash
# 1. Train on engineered features (you supply them).
curl -s $PREDICTALOT_URL/v1/tabular/train \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"modelId":"trend-3","backend":"lightgbm",
       "target":[[100,101,99,102,105,103,107,110,108,112]],
       "features":[{"rsi":[55,58,52,60,63,59,65,70,66,72],
                    "mom":[0.2,0.3,-0.1,0.4,0.5,0.2,0.6,0.7,0.4,0.8]}],
       "config":{"mode":"direction","horizon":3,"nEstimators":400}}' | jq

# 2. Forecast — LAST feature row is the anchor.
curl -s $PREDICTALOT_URL/v1/tabular/forecast \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"modelId":"trend-3","features":[{"rsi":[72],"mom":[0.8]}]}' | jq
# → {"modelId":"trend-3","backend":"lightgbm","mode":"direction","horizon":3,
#    "probUp":[0.63],"confidence":[0.26]}
```

For a driver that runs a univariate forecast and pretty-prints the interval, see [`scripts/predictalot.sh`](scripts/predictalot.sh):

```bash
PREDICTALOT_URL=http://localhost:8080 \
PREDICTALOT_AUTH_TOKEN=<token> \
  bash scripts/predictalot.sh chronos-2 5 10 11 12 13 14 15 16 17 18 19 20
```

## Tips

1. **Default to `chronos-2`** — fastest on CPU, widest type coverage (only model with future/both covariates), solid general-purpose accuracy.
2. **Skip or zero-weight `timesfm-2.5`** — weakest on every benchmark. In ensembles pass `weights={"timesfm-2.5":0}`.
3. **`moirai-2` is CC-BY-NC-4.0** — non-commercial. Fine for research/eval, not for a commercial product.
4. **Use `samples` for risk work** — `toto-1` / `sundial-base-128m` return raw `[series][sample][time]` paths; compute your own VaR / joint metrics instead of trusting fixed quantile cuts.
5. **`median` ≠ `quantiles["0.5"]` for chronos-2** — its `median` is the distribution mean; the others agree.
6. **Covariate length rules** — past covariates match the context length; future covariates match `horizon`; in the past+future type every future-cov name must also be a past-cov name.
7. **Tabular features are yours** — the API does no feature engineering. The LAST row per series is the forecast anchor.
8. **`overwrite: false` is the default** on every train endpoint — re-training a known `modelId` is a 409 until you pass `overwrite: true`.
9. **Discover, don't assume** — `GET /v1/timeseries/<type>/models` and `GET /v1/tabular/backends` are the live source of truth for membership and modes.
10. **First call is a cold load** — a model not yet resident pays a load (and download, if the snapshot isn't cached) on first request; subsequent calls are fast until the idle sweeper unloads it.
