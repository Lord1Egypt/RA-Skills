# SkillSpector audit — lygo-lattice-birth v1.0.0

**Signature:** Δ9Φ963-LATTICE-BIRTH-SKILLSPECTOR-v1.0.0

## Mitigations

| Finding | Mitigation |
|---------|------------|
| subprocess taint | Skill scripts use `_stack_tools.py` allowlist only |
| Unrestricted FS | `LYGO_STACK_ROOT` validated; path traversal blocked |
| Autonomous birth | Dual consent: human `--i-consent`; agents propose only |
| PII exposure | Gate rejects PII in public names; redaction on publish |

## Allowlisted stack tools

- `lygo_lattice_birth.py`
- `lygo_lineage_codec.py`
- `haven_star_chart_gate.py`

## Operator checklist

1. Set `LYGO_STACK_ROOT` to trusted clone.
2. `python scripts/self_check.py`
3. `python scripts/generate_mask.py` — inspect local output only.
4. Human approves before any `--i-consent` submit.