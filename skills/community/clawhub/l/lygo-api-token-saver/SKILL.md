---
name: lygo-api-token-saver
description: Minimize pay-to-go xAI/API token spend. Use when user says token saver, save tokens, API budget, pay-to-go burn, or before long Grok/Claude/GPT calls. Prefer local Ollama army; Biophase7 alt xAI key; compact agent behavior.
metadata: {"lygo": true, "budget": true, "ollama": true, "signature": "Δ9Φ963-TOKEN-SAVER-v1"}
---

# LYGO API token saver

## API key order (Biophase7)

1. **Never** paste keys in chat or commits.
2. Load vault: `python tools/load_biophase7_vault.py` → uses `XAI_API_KEY_ALT` before `XAI_API_KEY_MAIN`.
3. Frontier harness / probes: default `--models stack` only; add `grok` only when user explicitly needs frontier rows.
4. Set `LYGO_OPENAI_FRONTIER_MODEL` only when OpenAI runs are required.

## pxpipe-LYGO (vision context compression)

When prompts/tool dumps are huge and byte-exact hashes are not the focus:

```bash
cd lygo-protocol-stack
pip install -r requirements-pxpipe.txt
python tools/run_pxpipe_lygo_proxy.py
```

See `docs/BIOPHASE7_PXPIPE_LYGO.md` and skill `lygo-pxpipe-lygo`. Agent one-liner:

`python tools/pxpipe_lygo_for_agent.py --shrink-file <huge.txt> --target grok`

Do **not** compress secrets, seeds, or diff-critical line numbers.

## Prefer local silicon (zero API tokens)

```bash
# Ollama army cron + queue (127.0.0.1 only)
cd "%LYGO_STACK_ROOT%\.grok\skills\lygo-ollama-army\ollama_command_center\scripts"
python army_cron_once.py
```

- Drafting, summarizing repo files, grep/explore: **spawn_subagent explore** or **local Ollama** — not main chat API for bulk read.
- LFW path: `lyra_failsafe()` → `LYGO_LFW_FALLBACK_MODEL` on Ollama when cloud throttled.

## Agent behavior (Grok Build)

| Do | Don't |
|----|--------|
| Short replies; tables over prose | Re-summarize full session history |
| `grep` + `read_file` with `offset/limit` | `read_file` entire 3k-line trees |
| One `spawn_subagent` for execute batches | Many sequential full-context turns |
| `todo_write` only for 3+ steps | Narrate every tool call |
| Cache paths in one line ("see `path`") | Repeat URLs and commit hashes twice |
| `background: true` for HF push / long tests | Block chat on 10min uploads |
| Stop when task done | "Resonance forward" essays |

## Frontier harness (metered)

```bash
python tools/run_falsifiable_vector_test.py --load-vault --models stack
# API spend only if asked:
python tools/run_falsifiable_vector_test.py --load-vault --models grok --limit 3
```

Full 60× Grok ≈ high token + latency cost — require explicit user consent.

## User phrases → mode

- **"token saver" / "pay to go"** → stack-only tools, Ollama army, alt xAI, minimal chat output.
- **"push all"** → one subagent; don't re-read diff in main thread.

## Self-check

```bash
python -c "import os; print('alt' if os.environ.get('XAI_API_KEY_ALT') else 'no-vault')"
```

Install companion: `lygo-ollama-army`, `lygo-protocol-stack-operator`.