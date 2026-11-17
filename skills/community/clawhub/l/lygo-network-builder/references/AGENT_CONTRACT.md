# LYGO Network Builder — Agent Contract

**Signature:** Δ9Φ963-NETWORK-BUILDER-CONTRACT-v1.2

## MUST

- Load anchors from stack `docs/network_builder/IMMUTABLE_ANCHORS.json` (v1.2+) before citing URLs.
- Run `tools/lygo_network_builder_verify.py` (or `scripts/verify_anchors.py`) before declaring **LATTICE ALIGNED**.
- Report failed anchor `id` values from `tests/network_builder_last_run.json` on mismatch.
- Use `traversal_chants` from JSON for discovery; do not invent search strings.
- Read `references/SECURITY.md` on first use in a session.

## MUST NOT

- Simulate HTTP 200 checks.
- Publish, push git, HF, or ClawHub without explicit human consent.
- Treat Google Drive / Patreon links as automated health checks (`link_only`).
- Cite admin-only filesystem paths from anchor metadata in public output.

## Escalation

If local verify passes but user disputes public reality, chain:

1. `python tools/verify_lattice_alignment.py`
2. `python tools/verify_public_pages.py`

## Verdict language

| State | Say |
|-------|-----|
| `all_pass` + `LATTICE ALIGNED` | Anchors verified; cite JSON ids |
| failures on `http_required` | **NEEDS_FIX** + list ids |
| `http_soft` only | Note warnings; do not claim full outage |