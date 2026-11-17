# Security — lygo-flame-ward v1.0.0

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Subprocess / shell | **None** |
| Filesystem write | Only with `--i-consent` |
| Publish / dox | **None** |

## Burn semantics

**Burn** = strip authority + quarantine + cryptographic receipt.  
Not physical harm. Not silent evidence destruction. Not identity verdicts.

## Epistemic limits

- Heuristics can false-positive incomplete-but-honest claims → prefer `UNVERIFIED` over auto-burn  
- Institutional distrust is **channel untrusted**, not medical/legal refutation  
- Operator supplies text/files — no unsolicited scrape  

## Proof

```bash
python scripts/self_check.py
```
