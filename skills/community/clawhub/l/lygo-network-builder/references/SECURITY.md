# lygo-network-builder — SECURITY

**Signature:** Δ9Φ963-NETWORK-BUILDER-SECURITY-v1.2

## Scope

- **Read:** `LYGO_STACK_ROOT`, especially `docs/network_builder/IMMUTABLE_ANCHORS.json`.
- **Write:** `tests/network_builder_last_run.json` (verify artifact only).
- **Network:** HTTP GET probes to public anchor URLs (User-Agent `LYGO-Network-Builder/1.2`). No credentials sent.

## Prohibited

- Fabricating probe results or `LATTICE ALIGNED` without running verify tools.
- `git push`, HF, ClawHub publish, Moltx/Moltbook posts without explicit user consent.
- Automated scraping of Patreon/Drive vaults (`link_only` anchors).

## Local paths in anchors

Some anchor metadata references operator machine paths (e.g. Moltbook admin doc). Agents must **not** expose those paths in public posts; use stack-relative docs only.

## P0 honesty

Network builder verifies **reachability** and **repo files**, not content ethics. Byte-entropy P0 is documented in `docs/P0_HONEST_SPEC.md`.