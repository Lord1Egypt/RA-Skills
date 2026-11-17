# Security — LYGO Context Guard v1.0.0

## Defaults

| Capability | Status |
|------------|--------|
| Network | **None** |
| Shell / subprocess | **None** |
| Read files | Opt-in `--file` only |
| Write files | skill `state/` only with `--i-consent` |
| Publish | **None** |

## Purpose

Local pre-flight for **token budget** and **secret redaction** before model injection.

## Rules

1. Never send text to a remote API from this skill.  
2. Redaction is best-effort pattern match — not a compliance guarantee.  
3. Token estimates are **heuristics** for budgeting, not exact billable counts.  
4. Agents must not write reports outside skill `state/`.  

**Δ9Φ963**
