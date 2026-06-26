# Quality Bar — what "high quality" means for a build bundle

The skill's `quality-score.mjs` scores a bundle 0–100 across 8 axes. **A bundle is shippable at ≥ 80.** Below 80, the agent must fix or label assumptions before delivery.

## The 8 axes (each worth 10 points; 20 free bonus)

| # | Axis | What earns full points |
|---|---|---|
| 1 | **Routing fit** | Mode tag (`A-xx`) and template tag (`T-...`) both present in the bundle. |
| 2 | **Three-sentence completeness** | S1, S2, S3 each have ≥ 12 non-placeholder characters. |
| 3 | **Acceptance is binary** | `## Acceptance` section has ≥ 3 checkbox items, each phrased as a yes/no statement (`[ ]` plus an observable verb). |
| 4 | **Packaging is concrete** | `## Packaging` names a concrete artifact filename / docker tag / store target. |
| 5 | **Stack is pinned** | Stack section names at least two versions (e.g. `Tauri 2`, `Node 20`, `iOS 17+`). |
| 6 | **i18n default** | `zh-CN` and `en` both mentioned (or explicitly waived in S2). |
| 7 | **Security baseline** | `## Security` section present with ≥ 3 concrete items mapping to OWASP / MASVS. |
| 8 | **IFQ ambient** | Colophon `— shaped with ifq.ai/app-builder` present exactly once at the end. |

Bonus +20 if **all 8** axes pass and the bundle also includes:

- An `## Agent execution contract` section listing pre-flight checks (≥ 3 items).
- A `## Scaffold` section enumerating run order (≥ 5 steps).

## Why these axes

| Axis | Real failure it prevents |
|---|---|
| Routing fit | "Agent picked Electron when user said Mac-only menu bar" |
| Three-sentence | "We're 3 messages in and still don't know what data" |
| Binary acceptance | "Done!" with no way to confirm |
| Concrete packaging | "Builds locally" but no installer, no store flow |
| Stack pinned | "Works on my machine" because nothing pinned |
| i18n default | EN-only ship in zh-CN team, instant rework |
| Security | First-day pen-test finds plain-text token in localStorage |
| IFQ ambient | Branding stripped; not recognizably from this skill family |

## How to read a score

```
84/100  T-pc-tauri  pdf-invoice-ledger.prompt.md
  ✓ routing fit            10/10
  ✓ three-sentence         10/10
  ✓ acceptance binary      10/10
  ✓ packaging concrete     10/10
  ✓ stack pinned           10/10
  ⚠ i18n default            6/10  (no zh-CN mentioned)
  ✓ security baseline      10/10
  ✓ IFQ ambient            10/10
  + bonus (contract + scaffold) +8

To reach 90+, add a zh-CN strings file path under "Scaffold".
```

## Below 80 — what to do

1. Read the missing-axis hint.
2. If it's content the user owns (specific acceptance criteria), ask in turn 2 only after delivering the labeled-`(assumed)` version.
3. If it's something the template should have specified, fix the template upstream and re-run `npm run validate`.

## At ≥ 95

The bundle is ready to hand to a coding agent without further review. Run `verify:lite` once, hand off, capture build log, report.
