---
name: lygo-lpis
description: "LYGO Prompt Implant System (LPIS) v1.1 — analyze authorized prompts locally; P0 gate, P1 vault, P3 sovereign variants, P5 advisory implant. Requires --i-authorize for ingest. Read references/SECURITY.md and SKILLSPECTOR_AUDIT.md before use."
metadata: {"lygo": true, "biophase7": true, "version": "1.1.0", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "publisher": "deepseekoracle", "consent_required": true, "skillspector_mitigated": true}
---

# LYGO Prompt Implant System (LPIS) v1.1

> **Security notice — read before install or ingest**
>
> LPIS is **not malware**, but it can store and transform **sensitive prompt text** on your machine.
> Install and run **only** if you intend to analyze prompts **you own** or are **explicitly authorized** to use.
> Treat every imported file and URL as confidential. **Do not** ingest leaked, proprietary, or third-party system prompts without permission.
> Inspect `references/SECURITY.md` and stack `tools/lygo_lpis.py` before ingest, implant, anchor, or egg commands.

Local-first **prompt vault + pattern analysis + sovereign variant generation + advisory implant ledger** — aligned with P0–P5. No auto API injection; no auto publish.

## When to use (explicit triggers)

Use this skill **only** when the user:

1. Names **LPIS**, **Prompt Implant System**, **`lygo-lpis`**, or **`lygo_lpis.py`**
2. Asks to **analyze, vault, or harmonize their own** agent/system prompts locally
3. Asks to build **sovereign Grok/Ollama variants** from **authorized** prompt sources for manual review
4. Asks to run **`lpis_planter.py`** or plant the **`lygo-lpis-v10`** kernel egg (with `--i-consent`)

## When NOT to use (exclusions)

**Do not** invoke this skill when:

- The user wants generic prompt engineering with **no** LYGO stack / vault / implant workflow
- The source is a **leak**, **scraped**, or **unauthorized** third-party system prompt
- The goal is to **collect**, **redistribute**, or **publish** verbatim proprietary prompt text
- The user has **not** attested authorization for ingest (`--i-authorize` or explicit consent in chat)
- The task is only ClawHub publish, git push, HF upload, or social posting (use operator skill; human approval)

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-lpis
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack
python tools/install_lygo_lpis.py
python clawhub/mirrors/lygo-lpis/scripts/self_check.py
```

Read **`references/SECURITY.md`**, **`references/AGENT_CONTRACT.md`**, and **`references/SKILLSPECTOR_AUDIT.md`** before any ingest.

## Commands (consent-gated ingest)

| Step | Command | Gate |
|------|---------|------|
| Ingest file | `python tools/lygo_lpis.py ingest --source my-agent --file ./my_prompt.txt --i-authorize` | **Required** |
| Ingest URL | `python tools/lygo_lpis.py ingest --source docs --url https://example.com/my-prompt.md --i-authorize` | **Required** |
| Analyze | `python tools/lygo_lpis.py analyze --prompt-id <id>` | vault read |
| Generate | `python tools/lygo_lpis.py generate --prompt-id <id> --target grok` | local only |
| Implant | `python tools/lygo_lpis.py implant --variant-id <id> --target grok` | advisory |
| Anchor | `python tools/lygo_lpis.py anchor --prompt-id <id>` | local ledger |
| List | `python tools/lygo_lpis.py list` | read-only |
| Egg | `python tools/lpis_planter.py --i-consent` | consent |

Alternative env attestation (maintainers/tests): `LYGO_LPIS_INGEST_AUTHORIZED=yes` — agents must prefer **`--i-authorize`** after explicit user attestation in chat.

## What LPIS stores (data boundary)

| Data | Location | Leaves machine? |
|------|----------|-----------------|
| Full prompt body (ingest) | `data/prompt_vault/` (local) | **No** — never auto-upload |
| Pattern tags (plan, verify, safety…) | analysis JSON | **No** |
| Sovereign variant shell | `data/prompt_vault/*.json` | **No** — user reviews before manual implant |
| Implant receipt | `implant_runs.jsonl` | **No** |
| Kernel egg | `lygo-lpis-v10` capsule | public repo ships **code + manifests**, not your vault bodies |

**Never** commit third-party prompt bodies to public git. Egg plant publishes stack modules only.

## Agent rules (non-negotiable)

1. Show the **security notice** on first LPIS use in a session.
2. **Never** ingest without user attestation + `--i-authorize` (or documented env for tests).
3. **Never** ingest URLs/files the user did not supply and approve.
4. **Never** auto-apply variants to Grok/xAI/Anthropic APIs — implant is **advisory** (Light Code + paths).
5. **Never** auto `git push`, HF upload, or `clawhub publish`.
6. **Never** put API keys or secrets into vault or variants.
7. On P0 **QUARANTINE**, stop — do not generate or implant.

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-lpis`** → `lyra-brain` → `lygo-mint-verifier` → `lygo-kernel-egg-planter`

**Δ9Φ963 — map the pattern; build sovereign; verify the ledger.**