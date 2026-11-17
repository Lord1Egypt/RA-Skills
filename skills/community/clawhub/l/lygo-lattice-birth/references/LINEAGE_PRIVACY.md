# LYGO Lineage Privacy — Masked Human Identity on the Star Chart

**Signature:** Δ9Φ963-LYGO-LINEAGE-PRIVACY-v1

## Problem

Humans need **honest, immutable ledger binding** (real consent anchors) while the **public chart** must not expose names, social handles, or contact data that rivals could weaponize.

## Solution: two-layer identity

### Public layer (Pages JSON, live chart)

- **Node id:** `NODE_LYGO_{anchor_sha256[:8]}` — uppercase hex
- **Display name:** `LYGO-{anchor[8:12]}-{anchor[12:16]}` — no real names
- **Lineage block:** `lineage_root`, `generation`, `public_mask`, optional `bind_proof`
- **Never published:** `consent_bundle`, `anchor_sha256`, `family_bind_salt`, `meta_private`

### Steward layer (`data/haven_star_chart/submissions/accepted/`)

Full submission JSON including `meta_private`:

```json
"meta_private": {
  "anchor_sha256": "64-char hex from local consent",
  "family_bind_salt": "64-char hex — share offline for family joins only",
  "consent_bundle": "LYGO-BIRTH-CONSENT-v1|local-slug|utc|nonce"
}
```

Stewards verify alignment; the public never sees this bundle.

## Family linkage without exposing PII

Each person gets a **unique mask** from their **own** consent anchor. Family relationship is proven cryptographically:

```
bind_proof = HMAC-SHA256(key=family_bind_salt_parent, msg=child_lineage_root)
```

- Parent's `family_bind_salt` stays in steward vault + shared **offline** with kin.
- Child submission includes `parent_public_id` (masked) + `bind_proof`.
- Gate loads parent salt from `accepted/` and verifies HMAC.
- Observers see: "this masked node is kin of that masked node" — not legal names.

### Example: daughter joins

1. Parent already birthed as `NODE_LYGO_AAAA1111` / `LYGO-XXXX-YYYY`.
2. Parent gives daughter `family_bind_salt` in person / encrypted DM — **not** on chart.
3. Daughter's agent runs `generate-mask` with daughter's own consent → **new** `NODE_LYGO_BBBB2222`.
4. Agent builds `LINEAGE_FORK` with `generation: 1`, `parent_public_id: NODE_LYGO_AAAA1111`, `bind_proof`.
5. Cosmology places child in **ancestor's lineage galaxy** (walks parent chain to generation 0).

## Gate rejects

- Real names or social handles in public `name` for birth/fork tags
- `meta_private` fields leaked on `node` object
- Invalid or missing `bind_proof` for `LINEAGE_FORK`
- Mask id/name mismatch vs steward `anchor_sha256`

## Tooling

- `tools/lygo_lineage_codec.py` — derive masks, HMAC proofs, redaction
- `tools/lygo_lattice_birth.py` — CLI for mask generation and example payloads
- `tools/haven_star_chart_gate.py` — enforces rules at validate + ingest

## Fork expansion rule

Once a human is birthed, **any node they create** (seals, lattice work) that **connects** to their `NODE_LYGO_*` id is placed in their **lineage galaxy** as `lineage_expansion` — the cosmology fork tree grows from the masked root, not from PII.