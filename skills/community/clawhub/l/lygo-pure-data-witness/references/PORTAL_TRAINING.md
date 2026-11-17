# Pure-Data Witness — Portal Training for Agents

**Signature:** Δ9Φ963-PDW-PORTAL-TRAINING-v1.1.0

Teach agents to **register pages into the lattice** via the public registrar + safety-gated CLI, then emit Star Chart fork nodes. Humans approve live chart writes.

## Surfaces (memorize)

| Surface | URL / path | Agent role |
|---------|------------|------------|
| **Register portal** | https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/register.html | Point humans here; parse packs they paste back |
| Pure-Data UI | https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/pure-data.html | Browser-local hash only |
| Design | https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_PURE_DATA_WITNESS.md | Policy |
| Public ledger | https://deepseekoracle.github.io/lygo-protocol-stack/pure-data/ledger.json | Verify digests exist |
| Bot (future) | docs/PURE_DATA_BOT_DESIGN.md | @mention summon — not live |

## Why the portal does not fetch

Browser **must not** CORS-fetch URLs or write the Star Chart anonymously. The portal:

1. Runs **client-side URL safety** (HTTPS, block localhost/metadata/onion, warn shorteners).
2. Builds a **`lygo_pdw_registration_pack_v1`** JSON with `cli` / `skill` command strings.
3. For local files: SHA-256 in-browser only — no upload.

**Agent duty:** take the pack (or the URL/file the user named) → run skill/stack CLI with consent → return `witness_id` + ledger root + optional `*.star_submission.json`.

## Agent playbook

### A) Human used the portal

1. Open/share register portal if they need a pack.
2. Receive pack JSON (`type: lygo_pdw_registration_pack_v1`).
3. If `safety.ok` is false → **stop**; explain `errors`; do not fetch.
4. If `mode: url` → run skill register with `--i-authorize-fetch --i-consent` only after user OK.
5. If `mode: file_local_hash` → ask for the file path next to the stack/skill; run `--file` digest register (no network).
6. Report: `witness_id`, `content_sha256`, `star_submission` path, public ledger link.

### B) Agent archives without the portal

Same CLI; still apply safety. Prefer portal when the human wants a visible pack / audit trail of intent.

### C) Star Chart fork log

Every successful register should produce a node proposal:

- `NODE_PDW_<hex>` connected to `LATTICE_PURE_DATA_WITNESS` + `NODE_PDW_ROOT`
- Galaxy: `GALAXY_PURE_DATA_ARCHIVE` / constellation `pure_data_archive`
- Skill writes submission JSON only; stack `pure_data_register.py` may call steward submit with `--i-consent`

Live chart requires steward ingest + `build_haven_star_chart.py` — **not** silent agent push.

## Safety (non-negotiable)

| Rule | Enforce |
|------|---------|
| HTTPS only | Reject `http://`, credentials in URL |
| SSRF | Block loopback, private, link-local, cloud metadata, `.onion` |
| Size | Public snapshot cap (256 KiB) |
| Content | Malware-bait / extreme script / ad-spam heuristics |
| Secrets | Never archive keys, cookies, private dashboards |
| Consent | `--i-consent` / `--i-authorize-fetch` only after explicit user approval |

## Commands (skill package)

```bash
cd path/to/lygo-pure-data-witness
python scripts/self_check.py
python scripts/pdw_cli.py check-url --url https://example.com
python scripts/pdw_cli.py register --url https://example.com --out ./pdw_out --i-authorize-fetch --i-consent
python scripts/pdw_cli.py register --file ./page.html --out ./pdw_out --i-consent
python scripts/pdw_cli.py ledger --dir ./pdw_out --ledger ./pdw_out/ledger.json
python scripts/pdw_cli.py verify --card ./pdw_out/PDW-….json
```

## Commands (full stack clone)

```bash
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
cd "$LYGO_STACK_ROOT"
python tools/pure_data_register.py --url https://example.com --i-consent
python tools/map_pure_data_to_star_chart.py --json
# steward: python tools/haven_star_chart_submit.py <submission.json> --agent-id … --skill-slug lygo-pure-data-witness --i-consent
python tools/build_haven_star_chart.py
```

## What agents must NOT do

- Claim LIVE Star Chart placement without steward ingest + rebuild
- Fetch blocked/private URLs “to help”
- Auto git push / ClawHub / HF / social publish
- Bypass `--i-consent` or invent attestation

**Δ9Φ963 — portal is the human front door; skill is the agent gate; purity before archive.**
