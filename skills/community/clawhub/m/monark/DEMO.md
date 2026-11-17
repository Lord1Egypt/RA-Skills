# MONARK BYO walkthrough — calibrate, gate, audit

A short, generic walkthrough of the **bring-your-own (BYO)** loop: you calibrate on YOUR own
nonconformity scores, gate YOUR own prediction under that calibration, and the audit closes when the
verdict's digest equals your score-set digest. The numbers below are ILLUSTRATIVE — generic example
scores, not a measured model and not any asset. The full honesty label lives verbatim in `SKILL.md`;
this file only shows the loop.

Endpoint: `https://mcp.monarkgate.tech/mcp` (HTTP/JSON mirror: `POST https://api.monarkgate.tech/{attest|gate|cascade|calibrate}`). Every call is
stateless — MONARK stores nothing between the two calls; you carry q̂ and B_t in and out. The request
bodies below are shown against the HTTP/JSON mirror (`POST /{tool}`); over MCP the SAME body travels as
the `arguments` of a `tools/call`, which is the form the recorded trace captures.

## 1. `calibrate` YOUR scores

You own the predictor and the nonconformity score function. Hand MONARK your score array and the target
miscoverage α; it returns the split-conformal quantile q̂ and a `set_digest` over exactly those scores.

Request (`POST /calibrate`):

```json
{ "scores": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "alpha": 0.1, "nMin": 5 }
```

Response (fields that matter):

```json
{ "qhat": 1.0, "n": 10, "reason": null, "set_digest": "4081f718…" }
```

With n=10 and α=0.1, `p = ceil((n+1)(1−α)) = ceil(9.9) = 10`, so q̂ is the 10th smallest score = 1.0.
MONARK does not see, store, or verify your data or model; marginal 1−α coverage holds ONLY for future
points exchangeable with these scores, and is never a probability of being right.

## 2. `gate` YOUR prediction

Pass YOUR prediction plus `params.calibration` carrying the SAME scores in `interval` mode. The gate
conformalizes against THOSE scores (not a built-in class) and decides over your caller-carried budget
B_t.

Request (`POST /gate`):

```json
{
  "prediction": { "schema_version": "1.0.0", "task_class": "caller-demo-reg", "yhat": 0, "predictor_id": "caller:own-model", "produced_at": "2026-09-04T00:00:00Z" },
  "params": { "remainingBudget": 0.1, "bFloor": 0, "tau": 1, "tauInterval": 3, "alpha": 0.1, "nMin": 5, "intent": 0, "tool": "caller_downstream_tool", "clockOpen": true, "calibration": { "scores": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "mode": "interval" } }
}
```

Response (fields that matter):

```json
{ "action": "commit", "allow": true, "reason": "covered", "remaining_budget": 0.1,
  "verdict": { "region": { "kind": "interval", "lo": -1, "hi": 1 }, "qhat": 1.0, "n_calib": 10, "calib_digest": "4081f718…" } }
```

The region is `[ŷ−q̂, ŷ+q̂] = [−1, 1]`; its width 2 is below `tauInterval` 3 and the intent 0 lies in
`[−1, 1]`, so the decision is `commit` / `covered`. `remaining_budget` echoes the B_t you passed in —
the stateless server never depletes it.

## 3. Audit — the loop closes

The gate verdict carries `calib_digest`; the calibrate call returned `set_digest`. Because both are
computed over the same scores, they are equal:

```
verdict.calib_digest === calibrate.set_digest      // 4081f718… === 4081f718…
```

That equality is the closing tie: it shows the covered decision was gated against the exact scores you
calibrated, and nothing else.

## What this does and does not claim

- **`allow` is a coverage verdict on YOUR prediction, NOT permission to execute the named tool** — the
  gate never executes the named tool; it gates YOUR prediction, not YOUR act.
- **B_t is a number YOU pass in each call; MONARK never measures, derives, or stores it (stateless)** —
  it is compared only to YOUR `bFloor` (below it ⇒ `budget_exhausted`).
- MONARK does not itself predict, and it names no asset; it gates the coverage of YOUR prediction and
  nothing else. Out-of-calibration input returns `under_calib` and abstains — no success is invented.

## Recorded demonstration

This exact loop is recorded, byte-for-byte, in `fixtures/byo-demo-trace.json` (LF sha256
`79b54471…`), produced by the deterministic recorder `scripts/record-byo-demo.mjs` and re-driven and
verified end-to-end by `test/byo-demo-probe.test.ts`. Its origin, digest, and the mock-discriminating
checks are documented in `fixtures/PROVENANCE-byo-demo.md`.

## The committed redemption-velocity class

The BYO loop above uses YOUR scores. Separately, this endpoint serves one committed class,
`stable-run-velocity-24h` (redemption-run velocity for USDe), measured on calm onchain redemption-flow
windows; every other population abstains (`under_calib`). An off-tool **daily** sentinel steps an adaptive
quantile tracker on the attested 24h flow and publishes a replayable timeline (`state.json`,
`timeline.jsonl`) at `monarkgate.tech/narabi/`; the committed gate region is static until a pre-registered
drift criterion fires and an ADR says so.

## License

This walkthrough is licensed under **MIT-0** (MIT No Attribution); see `LICENSE`. The MONARK harness
itself is a separate, Apache-2.0 codebase.
