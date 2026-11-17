# SkillSpector notes — lygo-sanctuary-guardian v1.0.0

**Signature:** `Delta9Phi963-SANCTUARY-GUARDIAN`  
**Blueprint:** @grok

| Check | Status |
|-------|--------|
| subprocess / shell | Absent (AST self_check) |
| network / urllib | Absent |
| consent for writes | `--write` requires `--i-consent` |
| collapse default | Refused unless `--allow-collapse` |
| claim mismatch | SKILL.md denies physical barrier / firewall / TPM |
| tamper detect | verify-barrier fails on mutated truth |

```bash
python scripts/self_check.py
# expect ok · ast_clean · write_requires_consent · non_collapsing · tamper_detected
```
