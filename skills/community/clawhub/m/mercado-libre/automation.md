# Automation - Mercado Libre

Use this file when user asks to automate repetitive Mercado Libre workflows.

## Automation Principles

- automate only workflows with clear value and measurable risk reduction
- keep a manual fallback path for every critical flow
- require explicit confirmation before first live write execution

## Candidate Workflows

Typical automation targets:
- listing updates from structured inputs
- inventory and stock monitoring alerts
- order and incident status reconciliation
- periodic comparison and watchlist refresh jobs

## Safe Rollout Sequence

1. Define scope, boundaries, and failure conditions.
2. Run dry-check with sample data and expected outputs.
3. Execute first live run with narrow blast radius.
4. Reconcile results against panel-visible truth.
5. Expand only after consistent runs.

## Guardrails

- no hidden background actions outside declared scope
- no broad credential scopes when narrow scopes are enough
- no silent retries for risky write operations

## Output Template

```text
Workflow:
Scope:
Write actions involved:
Guardrails:
Rollback plan:
Go-live decision:
```
