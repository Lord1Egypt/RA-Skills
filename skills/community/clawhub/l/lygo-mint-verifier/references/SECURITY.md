# Security — lygo-mint-verifier v1.1.1

**Audit page:** https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier/security-audit

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Subprocess / shell | **None** (removed in 1.1.0) |
| Filesystem write | Ledgers under skill `state/` only with **operator-supplied** `--i-consent` |
| Publish | **None** — you paste Anchor Snippets yourself |

## ClawHub security-audit findings (resolved)

| Finding | Severity | Status | Fix |
|---------|----------|--------|-----|
| subprocess module call | Medium | **FIXED 1.1.0** | In-process `mint_cli.py`; no `subprocess` |
| Undeclared permissions / Lp3 | Medium | **FIXED 1.1.0** | Explicit metadata in SKILL.md + claw.json |
| Intent-Code Divergence (`backfill_anchors.py` auto-appends `--i-consent`) | Medium | **FIXED 1.1.1** | Wrapper is pass-through only |
| Description-Behavior Mismatch (compat wrapper defeats consent gate) | Medium | **FIXED 1.1.1** | Same — never rewrite `sys.argv` consent |

## Compat wrappers (must stay honest)

| Script | Behavior |
|--------|----------|
| `mint_pack_local.py` | Rewrites to `mint` subcommand; **does not** add `--i-consent` |
| `make_anchor_snippet.py` | Rewrites to `snippet` (read-only) |
| `backfill_anchors.py` | Rewrites to `backfill`; **does not** add `--i-consent` |

Ledger writes require the operator to pass `--i-consent` on the CLI (main or wrapper).

## Operator rules

- Never put API keys / tokens in packs
- Review pack content before minting
- Prefer skill-local `state/`; use `--state-dir` only on paths you control
- Prefer `python scripts/mint_cli.py …` as the primary entrypoint

## Proof

```bash
python scripts/self_check.py
# ok true · ast_clean · consent_wrapper_honest · mint/verify/snippet/backfill
```
