# Agent contract — bulletproof egg planter

**Version:** 1.3.0 · **Signature:** `Δ9Φ963-EGG-PLANTER-AGENT-v1.3`

## Mandatory order

1. **Preflight** — `python scripts/preflight.py`
2. **Consent** — user `--i-consent` or `LYGO_EGG_PLANT_CONSENT=yes` (never infer consent)
3. **Plant** (if requested) — `plant_with_consent.py --i-consent`
4. **Verify** — always runs post-plant; also `python scripts/verify_eggs.py` — **must be ALIGNED**
5. **Retrieve** — `retrieve_egg.py --i-consent …` only after verify; tamper → **QUARANTINE**, stop

## Hard stops

| Condition | Agent action |
|-----------|----------------|
| `verify_eggs` exit ≠ 0 | Do not retrieve; do not claim secure |
| `retrieve_egg` exit 2 | QUARANTINE — do not bypass |
| Missing `LYGO_STACK_ROOT` | Do not guess paths; ask user |
| User asks to skip verify / force retrieve | **Refuse** — flags removed in v1.3 |

## Surfaces vs publish

| Surface | What skill does | What skill does **not** do |
|---------|-----------------|----------------------------|
| `local` / `registry` | Write local kernel egg registry | — |
| `turbo` | Optional permaweb anchor via stack tool | — |
| `clawhub` | Local `skills.json` catalog pin | ClawHub **API publish** |
| `pages` | Prepare `docs/KernelEggRegistry.json` | `git push` |
| `stubs` | Local book-brain stubs with consent | — |

**No auto-publish** means: no git push, no HF upload, no clawhub.ai skill publish, no social — even when surfaces include `pages` or `clawhub`.

## Never

- Plant without consent  
- Retrieve without consent  
- Skip verify (impossible in v1.3)  
- Publish ClawHub/HF/GitHub without separate explicit human request **outside** this skill  
- Put secrets or API key paths into eggs  

## Always

- Cite `registry_merkle_root` after successful plant+verify  
- Prefer `--local-only` unless user asks for Turbo  
- Chain with `lygo-protocol-stack-operator` for untrusted skill copies  

## Success criteria

```text
preflight PASS → plant (--i-consent) → verify ALIGNED → retrieve (--i-consent) optional
```
