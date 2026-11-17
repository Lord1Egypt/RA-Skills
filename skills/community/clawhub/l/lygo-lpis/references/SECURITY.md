# SECURITY — LPIS v1.1

**Signature:** Δ9Φ963-LPIS-SECURITY-v1.1

## Purpose

LPIS helps **you** analyze and refactor **authorized** agent/system prompts into LYGO-aligned sovereign variants. It is a **local workflow tool**, not a prompt exfiltration or leak aggregator.

## User warnings (required reading)

1. **Authorization** — Ingest only prompts you **own**, **wrote**, or have **explicit permission** to analyze (employer policy, open license, your own exports).
2. **Prohibited sources** — Do **not** ingest leaked ChatGPT/Claude/Grok system prompts, competitor confidential docs, paywalled dumps, or scraped third-party agent configs.
3. **Sensitive handling** — Treat `data/prompt_vault/` as **confidential**. Exclude from backups/shares you do not control.
4. **Review before implant** — Generated variants include excerpts for review; apply manually in Grok project skills / agent instructions.
5. **Stack inspection** — Read `tools/lygo_lpis.py` and `lygo_lpis/` before running install, ingest, implant, anchor, or egg commands on an untrusted machine.

## Consent gates

| Action | Requirement |
|--------|-------------|
| Ingest file/URL | `--i-authorize` on CLI **or** `LYGO_LPIS_INGEST_AUTHORIZED=yes` after user attestation |
| Kernel egg plant | `--i-consent` on `tools/lpis_planter.py` |
| Git / ClawHub / HF / social | **Human explicit request only** — no agent auto-publish |

## Data handling limits

- **Max prompt size:** 2 MiB (P0 gate quarantines above cap)
- **P0 sample:** first 8–32 KiB entropy-checked
- **Variant shell:** truncates base excerpt at 12 KiB; full body stays in local vault only
- **URL ingest:** `urllib` fetch to user-supplied http(s) URL only; no background crawling
- **No telemetry:** LPIS does not phone home; no auto transmission to xAI/Anthropic/OpenAI

## Storage layout (local)

```
data/prompt_vault/
  vault_manifest.jsonl   # metadata only (sha256, provenance, ids)
  prompt_<id>.txt        # full body — KEEP PRIVATE
  prompt_<id>.json       # manifest shard
  sovereign_*.json       # generated variants
```

Add `data/prompt_vault/` to `.gitignore` discipline — **do not** commit vault bodies to public repos.

## Agent prohibitions

- No ingest without documented user authorization
- No chaining ingest → publish in one silent step
- No storing secrets in prompts, variants, or implant receipts
- No bypassing P0 QUARANTINE
- No recommending ingestion of "leaked" or "jailbreak" prompt packs

## Supply chain

- Install via official ClawHub: `deepseekoracle/lygo-lpis`
- Run `python scripts/self_check.py` after install
- Pin version in project docs; verify `metadata.version` matches expected release

## Incident response

If unauthorized prompt text was ingested:

1. Delete affected files under `data/prompt_vault/`
2. Remove lines from `vault_manifest.jsonl` for those ids
3. Do not publish or share variants derived from that ingest
4. Re-run `python tools/lygo_lpis.py list` to confirm removal