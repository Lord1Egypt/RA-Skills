# Agent contract — bulletproof egg planter

**Version:** 1.1.0 · **Signature:** `Δ9Φ963-EGG-PLANTER-AGENT-v1`

## Mandatory order

1. **Preflight** — `python scripts/preflight.py`
2. **Consent** — user `--i-consent` or `LYGO_EGG_PLANT_CONSENT=yes` (never infer consent)
3. **Plant** (if requested) — `plant_with_consent.py`
4. **Verify** — `python scripts/verify_eggs.py` — **must pass** (`ALIGNED`) before claiming success
5. **Retrieve** — only after verify pass; tamper → **QUARANTINE**, stop

## Hard stops

| Condition | Agent action |
|-----------|----------------|
| `verify_eggs` exit ≠ 0 | Do not retrieve eggs; do not tell user system is secure |
| `retrieve_egg` exit 3 | **TAMPER_DETECTED** — quarantine; do not decode inline payloads |
| Missing `LYGO_STACK_ROOT` | Do not guess paths; ask user |
| User asks to skip verify | Refuse for security-critical flows; explain four pillars |

## Never

- Plant without consent
- Publish ClawHub/HF/GitHub without separate explicit request
- Put secrets, tokens, or `boot/` key paths into eggs
- Replace stack `tools/verify_kernel_eggs.py` with a custom script without P0-gating the substitute

## Always

- Cite `registry_merkle_root` after successful plant+verify
- Point users to `docs/KERNEL_EGG_TAMPER_LOGIC.md` on GitHub for audit
- Chain with `lygo-protocol-stack-operator` P0 gate on **untrusted** skill downloads (not official clawhub install path)

## Success criteria

```text
preflight PASS → plant (consent) → verify_eggs verdict=ALIGNED → optional stubs/pages (user push)
```