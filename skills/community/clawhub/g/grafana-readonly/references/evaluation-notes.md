# Grafana Skill Evaluation Notes

## Current recommendation

Use `rpe-grafana` as the closest lightweight reference for read-only dashboard value retrieval.

Why:
- Focuses on existing dashboards and panels
- Lower operational scope than larger observability/Grafana suites
- Better fit for Grafana-first analytics Q&A

## Known likely gaps versus desired MVP

`rpe-grafana` appears to cover:
- list dashboards
- list panels
- query panel values

It likely does **not** fully cover:
- rich dashboard detail retrieval
- variable inspection
- explicit panel query extraction for explanation work
- flexible reruns with variable overrides comparable to a custom analytics workflow

## Why not lead with grafana-lens

`grafana-lens` appears broader, but also comes with:
- larger observability/alerts surface area
- more write/admin-oriented capability than needed
- higher review burden
- a weaker fit for business-side dashboard explanation work

## Practical path

1. Borrow the good read-only ideas from `rpe-grafana`
2. Keep our local skill tightly scoped
3. Add only the missing MVP actions we actually need
