---
name: lygo-pxpipe-lygo
description: Multi-tool vision context compression for LYGO (Anthropic, OpenAI, Grok/xAI, Gemini). Use before stuffing huge prompts or logs into pay-to-go APIs. Requires lygo-protocol-stack; read references/SECURITY.md. Agents run pxpipe_lygo_for_agent.py or local proxy — no auto publish/git push.
metadata: {"lygo": true, "biophase7": true, "version": "1.0.1", "requires_lygo_stack": true, "security_audit": "SkillSpector-hardened", "capability_filesystem_read": "LYGO_STACK_ROOT", "capability_filesystem_write": "data/pxpipe_lygo/manifests", "capability_subprocess": "tools/pxpipe_lygo_for_agent.py,tools/run_pxpipe_lygo_proxy.py", "capability_network": "localhost_47821_if_user_starts_proxy", "capability_git_publish": "human_only", "publisher": "deepseekoracle", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "signature": "Δ9Φ963-PXPIPE-LYGO-v1"}
---

# LYGO pxpipe-LYGO (ClawHub)

Sovereign **pxpipe**-style compression: bulky text → PNG for vision APIs, P0 gate, manifests under `data/pxpipe_lygo/`.

## When to use

- **Token saver** on large context (≥800 chars), not byte-exact secrets/hashes.
- Before pasting multi-KB tool dumps into Grok, Claude, or GPT.

## When not to use

- API keys, seeds, Merkle hashes, or line-precise diffs you must reproduce exactly.
- Unknown `LYGO_STACK_ROOT` or without reading `references/SECURITY.md`.

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-pxpipe-lygo
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
pip install -r "$LYGO_STACK_ROOT/requirements-pxpipe.txt"
```

## Agent commands (no proxy)

```bash
cd "$LYGO_STACK_ROOT"
python tools/pxpipe_lygo_for_agent.py --shrink-file path/to/huge.txt --target grok
python tools/pxpipe_lygo_for_agent.py --file path/to/huge.txt --target anthropic --png .pxpipe_ctx.png
```

## Multi-tool proxy

```bash
python tools/run_pxpipe_lygo_proxy.py
```

| Client | Base URL |
|--------|----------|
| Anthropic / Claude Code | `http://127.0.0.1:47821` |
| OpenAI SDK | `http://127.0.0.1:47821/v1` |
| Grok / xAI | `http://127.0.0.1:47821/v1` |

Set the matching API key in the environment. Proxy forwards upstream; does not store keys in manifests.

## Agent rules

1. Read `references/SECURITY.md` on first use.
2. Never compress secrets or `.env` contents.
3. No `git push`, ClawHub publish, or HF upload unless user explicitly asks.
4. Prefer `--shrink-file` in chat threads; use full JSON blocks only when building API calls.

## Skill chain

`lygo-api-token-saver` → **`lygo-pxpipe-lygo`** → `lygo-protocol-stack-operator`

## Doc

`docs/BIOPHASE7_PXPIPE_LYGO.md` in the stack repo.