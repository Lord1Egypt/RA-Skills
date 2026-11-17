# Security — LYGO Kickstart Wizard v1.0.0

## Trust boundary

- Onboarding and routing only.  
- Optional analysis imports **local** Ops Detector code if installed.  
- Lattice health uses **fixed HTTPS GET** endpoints only.

## Permissions

| Capability | Default |
|------------|---------|
| Network | Off except `lattice` intent (HTTPS GET allowlist) |
| Shell / subprocess | **Never** |
| Read files | Only paths you pass (`--text-file`, `--pack`) |
| Write | Only `--write` + `--i-consent` |
| Publish | **Never** |

## Threat controls

| Threat | Control |
|--------|---------|
| Auto-publish | Forbidden |
| SSRF | Fixed URL list |
| Shell injection | No subprocess |
| Covert exfil | No POST / no env dump |
| Misuse of ops detector | Consent + plain-English “not a person verdict” |

## Operator checklist

1. `python scripts/self_check.py`  
2. Prefer `map` before any analysis  
3. Do not feed private third-party mail without authority  

**Δ9Φ963**
