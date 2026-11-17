# LPIS agent contract

**Signature:** Δ9Φ963-LPIS-AGENT-CONTRACT-v1.1

Agents using `lygo-lpis` must follow this contract.

## Before first use

1. Display the **Security notice** from `SKILL.md` (authorization + no leaked prompts).
2. Confirm the user owns or is authorized to analyze the prompt source.
3. Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

## Allowed operations

| Operation | Preconditions |
|-----------|---------------|
| `ingest` | User attestation + `--i-authorize`; user-supplied path or URL only |
| `analyze` / `list` | Read local vault metadata |
| `generate` | Authorized ingest already in vault; P0 not QUARANTINE |
| `implant` | User chose target; output is advisory receipt only |
| `anchor` | Local ledger write |
| `lpis_planter.py` | `--i-consent` |

## Forbidden operations

- Ingest without authorization flag or env attestation
- Ingest from "leaked prompts" repositories or scraped competitor system prompts
- Auto-apply variants to remote LLM project settings
- `git push`, HF upload, `clawhub publish`, social post without explicit user request
- Store API keys, tokens, or credentials in vault or variants
- Continue after P0 QUARANTINE

## Failure handling

| Error | Action |
|-------|--------|
| `ingest_not_authorized` | Ask user to attest ownership; retry with `--i-authorize` |
| `p0_quarantine` | Stop; do not generate/implant; report reason |
| `not_found` | Verify `list` and prompt_id |

## Session handoff

After implant sessions, optionally pair with **`lyra-brain`** for snips — vault bodies stay out of public memory unless user consents.