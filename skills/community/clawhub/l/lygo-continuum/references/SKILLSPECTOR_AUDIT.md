# SkillSpector audit response — lygo-continuum v1.0.1

**Source:** https://clawhub.ai/deepseekoracle/skills/lygo-continuum/security-audit

## Findings addressed

| Finding | Severity | Fix in 1.0.1 |
|---------|----------|--------------|
| Quickstart pushes remote portal vs “pure local / no network” | Medium | Quickstart is **local-first**; portal is **optional separate site** with trust warning; CLI docstring states it never opens network |
| `--out` writes anywhere while docs imply state/`--i-consent` only | High | `authorize_write()`: under `--base`, or `state/` + `--i-consent`, or explicit `--i-allow-any-out` |
| Glob / paths can escape base via `..` or absolute patterns | Medium | `resolve_path` + `safe_glob` reject absolute/`..`; matches filtered under base |

## Residual

- Operator who passes `--i-allow-any-out` can write anywhere (explicit).  
- Capsules from untrusted authors should still be reviewed before verify.  

```bash
python scripts/self_check.py
```

**Δ9Φ963**
