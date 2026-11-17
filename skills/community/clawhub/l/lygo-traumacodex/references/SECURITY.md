# Security — lygo-traumacodex 1.0.2 (ClawHub public)

## Audit response (SkillSpector findings addressed)

| Finding | Fix in 1.0.2 |
|---------|----------------|
| subprocess to external tool | **Removed.** No `subprocess` module usage. |
| `LYGO_STACK_ROOT` → code exec | **Removed.** Env is ignored; no external script loading. |
| Tool poisoning / outside package | All logic in `scripts/traumacodex_core.py` inside this package. |
| Missing permissions | Declared in `claw.json` → `permissions`. |
| Vague triggers | SKILL.md / description: when to run + not medical. |

## Guarantees

- **No network**
- **No subprocess / shell**
- **No eval/exec of user code**
- **No raw IBI stored** in packages (hash only)
- **Not medical** — digests are protocol seals only

## Writes

| Flag | Destination |
|------|-------------|
| default | `./traumacodex_out` under current working directory |
| `--out DIR` | User-chosen directory |
| `--i-consent` without `--out` | skill `state/` only |

## FULL stack channel

Operator stack `tools/traumacodex_waveform.py` (P7/P8 modules, living-mesh badge) is **not** executed by this public skill. It lives on the LYGO stack / SkillHub FULL vault and is out of this package’s security boundary by design.
