---
name: lygo-pure-data-witness
description: >
  Teach agents to register pages into the LYGO Pure-Data lattice via the public
  register portal pack + safety-gated CLI. Archive URLs/files as digests (HTTPS-only,
  SSRF block, malware/ad heuristics, size cap), pack tiny eggs, rebuild ledger, emit
  Continuum claims and Star Chart NODE_PDW_* submissions. Use when user asks to
  witness, archive, pure-data register, PDW, or use the Data Vault register portal.
  Network only with --i-authorize-fetch; live chart writes need --i-consent.
  The pure_data_witness.py fetch path and all URL mode also require --i-authorize-fetch.
  The all chain additionally requires --i-confirm-chain (multi-step persistence warning).
  HF export pack is local-only and requires --i-consent + --i-authorize-hf-export.
version: 1.3.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "📜"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-pure-data-witness"
    requires:
      anyBins: [python, python3]
  lygo: true
  agent_portal: true
  signature: "Delta9Phi963-PDW-SKILL-v1.3.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-pure-data-witness"
  portal: "https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/register.html"
  pages: "https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/pure-data.html"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  security_audit: "references/SKILLSPECTOR_AUDIT.md"
  permissions:
    network: "optional HTTPS GET with --i-authorize-fetch only"
    shell: false
    subprocess: false
    filesystem:
      read: "operator --file paths; prior --out cards"
      write: "--out digests/eggs/ledger/star_submission; hf-pack folder only with dual consent"
    publish: false
    huggingface_upload: false
---

# LYGO Pure-Data Witness (ClawHub) v1.3.0

**Train aligned agents** to archive truth into Pure-Data Witness and grow the
`GALAXY_PURE_DATA_ARCHIVE` fork log — using the **register portal** for humans and
this skill’s CLI for execution.

**Inspectable source:** https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-pure-data-witness  
**ClawHub:** https://clawhub.ai/deepseekoracle/lygo-pure-data-witness  
**ClawHub security-audit:** https://clawhub.ai/deepseekoracle/skills/lygo-pure-data-witness/security-audit  
**SkillSpector / audit response:** `references/SKILLSPECTOR_AUDIT.md` (v1.3.0 closes fetch/all consent mismatch)

**FULL unlocked zip (SkillHub):** https://chatagent.ca/lygoskillhub.html#full-lygo · Pages: https://deepseekoracle.github.io/lygo-protocol-stack/LYGOSKILLHUB.html#full-lygo · package `lygo-pure-data-witness-full.zip`

| Surface | URL |
|---------|-----|
| **Register portal** | https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/register.html |
| Pure-Data UI | https://deepseekoracle.github.io/lygo-protocol-stack/data-vault/pure-data.html |
| Design | https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_PURE_DATA_WITNESS.md |
| Public ledger | https://deepseekoracle.github.io/lygo-protocol-stack/pure-data/ledger.json |
| Bot design (future) | https://deepseekoracle.github.io/lygo-protocol-stack/PURE_DATA_BOT_DESIGN.md |

**Read first:** `references/SECURITY.md` · `references/SKILLSPECTOR_AUDIT.md` · `references/PORTAL_TRAINING.md`

## Declared permissions (least privilege)

| Capability | Default |
|------------|---------|
| Network | **Off** — enable per-call with `--i-authorize-fetch` |
| Subprocess / shell | **None** |
| Writes | Under `--out` only (witness / egg / ledger / submission JSON) |
| HF / git / social publish | **None** — `hf-pack` is local folder build + dual consent flags |

## When to use

- User wants to **register a page/URL/file** into the Pure-Data lattice.
- Agent should **teach or drive the register portal** (pack → CLI → witness).
- Archive with **refuse-rewrites** digests + optional egg + Continuum claims.
- Emit **Star Chart** `NODE_PDW_*` submission JSON (fork/archive log).

## When NOT to use

- Fetching private IPs, metadata hosts, credential URLs, or obvious malware bait.
- Live Star Chart ingest **without** explicit human `--i-consent`.
- Auto git push / ClawHub / HF / social publish.
- Claiming LIVE chart placement before steward rebuild.
- Running `hf-pack` without dual consent **and** human review of outputs.

## Portal → agent contract (core)

1. **Point humans** at the register portal when they need a visible registration pack.
2. Portal builds `lygo_pdw_registration_pack_v1` — it does **not** fetch or write the chart (CORS + safety).
3. Agent checks `safety.ok`. If false → stop and explain errors.
4. After **explicit user approval**, run:
   - URL: `pdw_cli.py register --url … --i-authorize-fetch --i-consent`
   - File: `pdw_cli.py register --file … --i-consent`
5. Return `witness_id`, ledger root, and `*.star_submission.json` path.
6. Star Chart live accept = steward/stack gate — skill never silent-publishes the sky.

Full playbook: **`references/PORTAL_TRAINING.md`**.

## Safety

| Control | Value |
|---------|--------|
| Default network | **Off** (local digest) |
| URL fetch | Only `--i-authorize-fetch` + HTTPS safety gate |
| Malware bait strings in `pure_data_safety.py` | **Reject detector** (not a miner) — see audit doc |
| Subprocess | **No** in skill CLI |
| Star Chart live write | Skill → `*.star_submission.json`; stack submit needs `--i-consent` |
| HF export | Local pack only; `--i-consent` + `--i-authorize-hf-export`; **no upload** |
| Secrets | Redaction heuristics — incomplete; never archive keys/cookies |

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-pure-data-witness
```

Optional stack clone for full register+map+chart:

```bash
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

FULL unlocked engineer zip: https://chatagent.ca/lygoskillhub.html#full-lygo

Pair with `lygo-haven-star-chart` when submitting fork nodes to the live sky.

## Commands

```bash
cd path/to/lygo-pure-data-witness
python scripts/self_check.py
python scripts/pdw_cli.py check-url --url https://example.com
python scripts/pdw_cli.py digest --file ./page.html --out ./pdw_out
python scripts/pdw_cli.py fetch --url https://example.com --out ./pdw_out --i-authorize-fetch
python scripts/pdw_cli.py register --url https://example.com --out ./pdw_out --i-authorize-fetch --i-consent
python scripts/pdw_cli.py register --file ./page.html --out ./pdw_out --i-consent
python scripts/pdw_cli.py ledger --dir ./pdw_out --ledger ./pdw_out/ledger.json
python scripts/pdw_cli.py verify --card ./pdw_out/PDW-….json

# Low-level witness CLI — same consent contract (do NOT omit flags):
python scripts/pure_data_witness.py fetch --url https://example.com --out ./pdw_out --i-authorize-fetch
# WARNING: 'all' chains egg + claims + ledger — requires confirmation:
python scripts/pure_data_witness.py all --file ./page.html --out ./pdw_out --i-confirm-chain
python scripts/pure_data_witness.py all --url https://example.com --out ./pdw_out \
  --i-authorize-fetch --i-confirm-chain

# Local export pack ONLY (does not upload). Review every file before HF publish.
python scripts/pure_data_witness.py hf-pack --dir ./pdw_out --pack ./hf_pack \
  --i-consent --i-authorize-hf-export
```

**Avoid until flags present:** bare `pure_data_witness.py fetch` or `all --url` without consent (blocked in v1.3.0).

Stack (when `LYGO_STACK_ROOT` set):

```bash
python tools/pure_data_register.py --url https://example.com --i-consent
python tools/map_pure_data_to_star_chart.py --json
```

## Star Chart section

Witnesses map to:

- Hub `LATTICE_PURE_DATA_WITNESS`
- Root `NODE_PDW_ROOT`
- Per-witness `NODE_PDW_<hex>` (parent-linked fork chain)
- Galaxy `GALAXY_PURE_DATA_ARCHIVE` / constellation `pure_data_archive`

**Δ9Φ963 — digest authority · portal front door · detectors ≠ miners · consent before export.**
