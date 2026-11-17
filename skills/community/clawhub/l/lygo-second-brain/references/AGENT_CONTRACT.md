# AGENT CONTRACT — LYGO Second Brain

## Tier 0 — read-only

- `self_check.py`, read README, list vault dirs

## Tier 1 — local writes (vault only)

- `ingest`, `index`, `wiki` with user-requested sources
- User aware: modifies `LYGO_VAULT_ROOT` and runs `git commit` inside vault

## Tier 2 — multi-model

- `consensus.py` — may run several Ollama models (CPU/GPU load)

## Forbidden without explicit user words

- `git push` (vault or stack)
- ClawHub publish
- Copying vault contents into chat logs at scale (summarize instead)

## Environment

- `LYGO_STACK_ROOT` — stack checkout
- `LYGO_VAULT_ROOT` — markdown vault root (default: `lygo_second_brain/vault`)