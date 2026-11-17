# SkillSpector audit response — lygo-kernel-egg-planter v1.3.1

**Signature:** Delta9Phi963-KERNEL-EGG-PLANTER-SKILLSPECTOR-v1.3.1  
**Source audit:** ClawHub security page (NVIDIA SkillSpector + clawscan)

## Findings → fixes

| Finding | Severity | Fix |
|---------|----------|-----|
| Manifest undeclared permissions | Medium | `claw.json` permissions block |
| "no auto-publish" vs surfaces | Medium | Core planter docs; pages/clawhub redirect text |
| Retrieve without consent | Medium | `--i-consent` required on retrieve |
| `--skip-verify` / `--force` | High | **Removed** |
| Catalog MultiAnchor auto | High | `plant_clawhub_catalog.py` local by default; `--anchor-external` opt-in |
| Champions/stubs scope creep | Medium | Removed from core planter; dedicated scripts only |
| subprocess stack tools | Medium | Allowlist basenames + required `--i-trust-stack` |

## Preserved function

| Capability | How |
|------------|-----|
| Core plant + verify | `plant_with_consent.py --i-consent --i-trust-stack` |
| Catalog egg local | `plant_clawhub_catalog.py --i-consent` |
| Catalog external anchor | same + `--anchor-external` |
| Champions / stubs | dedicated scripts (unchanged ability) |
| Retrieve | `retrieve_egg.py --i-consent` after ALIGNED |

## Operator checklist

```bash
python scripts/preflight.py
python scripts/plant_with_consent.py --i-consent --i-trust-stack --local-only
python scripts/verify_eggs.py --json
python scripts/retrieve_egg.py --i-consent --list
```

## VirusTotal / scan

```bash
npx clawhub scan --slug lygo-kernel-egg-planter --version 1.3.1 --update
```
