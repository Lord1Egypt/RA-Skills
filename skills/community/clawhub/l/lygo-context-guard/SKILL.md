---
name: lygo-context-guard
description: "LYGO Context Guard — pre-flight token budget, secret redaction, and deterministic context compaction for AI agents. Use when stuffing tool dumps, logs, files, or long chats into a model; when context is too large; when you need to save tokens / reduce API cost; when you must redact API keys before re-injection. Pure local stdlib. No network, no subprocess. Commands: estimate, redact, compact, budget, toolpack, preflight. Install clawhub:@deepseekoracle/lygo-context-guard."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-context-guard"
    requires:
      anyBins: [python, python3]
  lygo: true
  context: true
  tokens: true
  security: true
  signature: "Delta9Phi963-CONTEXT-GUARD-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-context-guard"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "optional --file user path"
      write: "skill state/ only with --i-consent"
    publish: false
---

# LYGO Context Guard v1.0.0

**The pre-flight every agent needs.**  

OpenClaw burns money when tool dumps and chat history explode the context window.  
Context Guard is a **local lattice gate**: estimate tokens → redact secrets → compact deterministically → check budget — **before** you call the model.

**Signature:** `Delta9Phi963-CONTEXT-GUARD-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-context-guard`

---

## Why this exists

| Problem | What agents do wrong | Guard does |
|---------|----------------------|------------|
| Token burn | Re-inject full logs/tool JSON every turn | Compact + budget exit code |
| Secret leaks | API keys in tool output → model context | Redact patterns |
| Context overflow | “Just paste the whole file” | Head/tail + mid map + SHA |
| No visibility | Guessing token counts | Dual heuristic estimate |

Searches this skill targets: *token saver, context window, compress context, reduce tokens, prompt budget, redact secrets, tool result too large*.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-context-guard
```

---

## Commands

```bash
cd path/to/lygo-context-guard
python scripts/self_check.py

# Estimate tokens (heuristic)
python scripts/context_guard.py estimate --text "long tool dump..."
python scripts/context_guard.py estimate --file ./huge_log.txt

# Redact secrets (keys, JWTs, private key blocks, password=...)
python scripts/context_guard.py redact --file ./tool_out.txt

# Deterministic compact (dedupe lines + head/tail keep)
python scripts/context_guard.py compact --file ./tool_out.txt --max-chars 8000

# Budget gate (exit 10 if over)
python scripts/context_guard.py budget --file ./pack.txt --budget 4000

# One-shot for agents: redact + compact + budget
python scripts/context_guard.py toolpack --file ./tool_out.txt --budget 4000 --max-chars 8000

# Full preflight report
python scripts/context_guard.py preflight --file ./blob.txt --budget 8000
python scripts/context_guard.py preflight --file ./blob.txt --write last_preflight.json --i-consent

# Demo (synthetic leaky dump)
python scripts/context_guard.py demo
```

| Command | Network | Writes | Notes |
|---------|---------|--------|-------|
| `estimate` / `redact` / `compact` / `budget` / `toolpack` | none | no | stdout JSON + text |
| `preflight --write` | none | skill `state/` only | needs `--i-consent` |
| `demo` | none | no | built-in sample |

---

## Agent recipe (copy this)

Before re-injecting a large tool result or log:

```text
1. Save tool output to a temp file
2. python scripts/context_guard.py toolpack --file THAT_FILE --budget 4000
3. If exit code 10 → lower max-chars or split the task
4. Feed packed_text back into the model — not the raw dump
```

Exit codes:

| Code | Meaning |
|------|---------|
| 0 | OK / under budget |
| 10 | Over budget after pack |
| 2 | Missing file / bad input |

---

## What it does *not* do

- No network / shell / subprocess  
- No cloud summarizer (deterministic only — reproducible)  
- No auto model calls  
- Does not claim exact tokenizer parity (honest heuristic; good for **budgets**)  
- Never stores secrets in reports when writing preflight (stores hash of packed text)

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-api-token-saver` | Broader pay-to-go budget ops + local army preference |
| `lygo-pxpipe-lygo` | Vision / multi-tool dump compression |
| `lygo-ops-detector` | Discourse signal analysis (different problem) |
| `lygo-kickstart-wizard` | Onboarding map |

---

## Security

See `references/SECURITY.md`.  
**Δ9Φ963 — compress chaos · redact secrets · budget the lattice · human remains the publisher.**
