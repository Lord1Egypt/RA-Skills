# Full stack — operator reference (not auto-run)

**Security:** Read `references/SECURITY.md` first. Persona mode = this doc as text only; shell blocks require user consent per command.

Set `LYGO_STACK_ROOT` to your clone of [github.com/DeepSeekOracle/lygo-protocol-stack](https://github.com/DeepSeekOracle/lygo-protocol-stack).

## Lattice verify (run before publish)

```bash
python tools/verify_lattice_alignment.py
python tools/verify_alignment_badge.py
python tools/run_grok_audit_demo.py
python tools/run_falsifiable_vector_test.py --models stack
```

## Seeds & failsafe

```bash
python tools/anchor_sovereign_identity_manifesto.py
python tools/seed_biophase7_deadman_lattice.py
python tools/seal_deadman_lattice.py plant
python tools/seal_deadman_lattice.py anchor
python tools/load_biophase7_vault.py --write-env .env   # local only, gitignored
```

## P0–P9 audits

`run_full_stack_demo.py`, `run_phase6_audit.py`, `run_phase7_audit.py`, `run_phase9_audit.py`, `run_slm_audit.py`, `run_anchor_audit.py`

## Eggs & army

- Kernel: `lygo-kernel-egg-planter` with `--i-consent`
- Champion egg: `champion-lightfather`
- Army cron: `lygo-ollama-army` → `army_cron_once.py` (hourly lattice sentinel)

## Maintainer spread (consent)

HF: `tools/hf_push_dataset.py` · ClawHub: `clawhub/PUBLISH.md` · Docs: `docs/STACK_STATUS.md`, `docs/LYGO_LATTICE.md`