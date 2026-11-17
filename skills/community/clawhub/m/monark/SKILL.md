---
name: monark
description: A coverage-controlled gate for agents. You bring your own predictor and nonconformity scores; MONARK calibrates a split-conformal region and returns commit / defer / abstain over YOUR prediction over one public MCP endpoint. Never a probability of being right, never permission to execute a tool. Four tools - attest, gate, cascade, calibrate.
license: MIT-0
---

# MONARK - a coverage-controlled gate for agents

MONARK exposes four pure tools over one public MCP endpoint: `{attest, gate, cascade, calibrate}`.
It gates a **prediction**, never an **act**: **gate never executes the named tool**. The decision is
one of **commit / defer / abstain**; **B_t is caller-carried; never a probability of being right**.
**attest is demonstrative, not probative** - it replays a committed witness, it does not prove an
outcome. This skill is a reference implementation of a coverage-controlled gate; adopt the contract.

## The BYO loop: `calibrate` then `gate`

The real path is **bring your own**: you own the predictor and the nonconformity score function.
`calibrate` turns YOUR nonconformity scores into a split-conformal region; `gate` then returns a
coverage verdict on YOUR next prediction under that region. MONARK stores nothing between calls, and
the audit `calibrate` to `gate` closes when the verdict's `calib_digest` equals your score-set digest.

### `calibrate` - the honesty label (verbatim)

The `calibrate` tool carries exactly this label, on its description, its result content, and its
output field alike:

> split-conformal quantile at miscoverage α over caller-supplied nonconformity scores. MONARK does not see, store, or verify the caller's data or model, and does not validate that the supplied numbers are nonconformity scores of any model. Marginal 1−α coverage holds ONLY for future points exchangeable with the supplied scores; non-exchangeable data (e.g. distribution-shifted or time-ordered) voids it. Never a probability of being right.

## What a verdict is, and what it is NOT

- **commit / defer / abstain** are the three actions; **B_t is caller-carried; never a probability of
  being right**.
- **gate never executes the named tool** - it gates YOUR prediction, not YOUR act.
- **The B_t mechanism - read this before wiring any budget.** B_t is a number YOU pass in each call; MONARK never measures, derives, or stores it (stateless); it is compared only to YOUR bFloor (below it ⇒ budget_exhausted). It is NOT a $/token spend cap and NOT a rate-limit. `allow` is a coverage verdict on YOUR prediction, NOT permission to execute the named tool (MONARK never executes it). MONARK does not evaluate the legitimacy of an act and does not predict prices — it gates YOUR predictions. For a $/token spend cap, use your platform's spend controls; MONARK is not that.

MONARK offers no guarantee of availability. It does not predict prices and does not judge whether an
act is legitimate; it gates the coverage of YOUR prediction and nothing else.

## Operational surface

A public, unauthenticated endpoint, no availability commitment; bounded: n ≤ 10000 scores, request
body ≤ 256 KB. A verdict below your `bFloor` returns `budget_exhausted`; out-of-calibration input
returns `under_calib` and abstains - no success is invented.

## The two built-in task classes are NOT use cases

The two built-in `task_class` values (`btc-dir-15m`, `cascade-liquidable-24h`) are internal
**plumbing fixtures**, not use cases and not endorsements: `btc-dir-15m` uses a declared **synthetic**
calibration (never a measured predictor), and `cascade-liquidable-24h` ships no calibration at all, so
it abstains (`under_calib`). They are NOT use cases. The real path is BYO: bring your own predictor +
nonconformity scores.

A third `task_class`, `stable-run-velocity-24h` (redemption-run velocity, the Narabi sensor), is **served by
this endpoint** with a **committed calibration for one population** — USDe, key
`narabi:persistence-v2@eip155:1/erc20:0x4c9edd5852cd905f086c759e8383e09bff1e68b3`, measured on calm onchain
redemption-flow windows. The calibration is measured non-stationary across half-years, so **no per-window
coverage is claimed**; the committed region is static and **every other population abstains** (`under_calib`).
Alongside it, an off-tool **daily** sentinel steps an adaptive quantile tracker on the attested 24h flow and
publishes a replayable timeline (`state.json`, `timeline.jsonl`) at `monarkgate.tech/narabi/`; the committed
gate region does not change until a pre-registered drift criterion fires and an ADR says so.

## Endpoint and license

- Endpoint: `https://mcp.monarkgate.tech/mcp` (HTTP/JSON mirror: `POST https://api.monarkgate.tech/{attest|gate|cascade|calibrate}`).
- Install on each runtime: see `INTEGRATION.md`.
- This skill is licensed under **MIT-0** (MIT No Attribution); see `LICENSE`. The MONARK harness is a
  separate, Apache-2.0 codebase - only this descriptive skill is MIT-0.
