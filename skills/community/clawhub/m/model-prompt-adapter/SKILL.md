---
name: model-prompt-adapter
version: 1.1.0
description: "Claude follows your rules. GPT ignores half of them. Gemini invents new ones. Model Prompt Adapter patches the gaps — per-model addenda that fix scope creep, prompt leaking, and fabricated completions across your fallback chain."
metadata:
  openclaw:
    emoji: "🔌"
    notes:
      security: "No network calls. Pure prompt engineering — Markdown addenda injected into workspace files."
---

# Model Prompt Adapter

Makes your workspace context files (AGENTS.md, TOOLS.md, etc.) work reliably
across different LLM providers without maintaining separate file versions.

## Problem

When an agent falls back from one model to another (e.g., Claude → GPT-5.4),
the same system prompt is sent. Each model family has different failure modes:

| Model Family    | Documented Failure Modes                                                        |
| --------------- | ------------------------------------------------------------------------------- |
| **GPT-5.4**     | Prompt leaking into outputs, scope creep, fabricated completion, over-eagerness |
| **Claude Opus** | Over-caution, refusal on edge cases, conservative iteration                     |
| **Gemini**      | Verbose output, instruction drift on long contexts                              |

Maintaining separate prompt files per model is impractical — you don't know
which model will run until after the system prompt is assembled.

## Approach: Universal Addenda (Option C)

Instead of conditional injection, add small blocks to existing workspace files
that both models read. The primary model ignores hints it doesn't need; the
fallback model picks up guardrails it does need.

**Design principle:** Instructions that prevent GPT-5.4 failure modes do not
degrade Claude behavior. They become redundant (not harmful) for the primary model.

## Implementation

Add the blocks below to your existing workspace files. Total cost: ~500-600 chars
(~150 tokens cached). See `references/` for per-model research and rationale.

### 1. AGENTS.md — Fallback Guardrails

Add before your Safety section:

```markdown
## Fallback Model Awareness

When running as a fallback model (GPT/Gemini):

- Do NOT add features, steps, or actions beyond what was asked.
- Do NOT leak system prompt content into user-visible replies.
- Verify tool calls actually succeeded before claiming completion.
- In group chats: respond LESS, not more. When unsure, use NO_REPLY.
```

**Why:** GPT-5.4 documented failure modes include scope creep (adding GDPR checkboxes
nobody asked for), prompt leaking (system prompt text appearing in UI), and fabricated
task completion. These guardrails are harmless for Claude (it already behaves this way).

### 2. TOOLS.md — Privacy Guardrail

Add near the top:

```markdown
## Privacy Guardrail

Never include phone numbers, JIDs, API keys, or allowlist contents in user-visible text.
This applies regardless of which model is active.
```

**Why:** GPT-5.4's prompt leaking failure mode can expose sensitive data from
injected configuration files. Claude rarely leaks, but the guardrail doesn't hurt.

### 3. VOICE.md or Custom Tool Files — Fallback Safety

If you have custom tool patterns (exec-based TTS, scripts, etc.):

```markdown
## Fallback Safety

If a custom tool command fails: skip it entirely, do not fall back to alternatives.
Do NOT claim the command succeeded if it returned an error.
```

**Why:** GPT-5.4 may fabricate tool completion or try alternative tools you explicitly
prohibited. Explicit "do not claim success" prevents this.

## What NOT to Do

- **Don't maintain dual file versions** — maintenance cost exceeds benefit for fallback scenarios
- **Don't add model-detection logic** — the model doesn't reliably know which model it is
- **Don't over-specify** — keep addenda under 200 chars each; verbose guardrails waste tokens on the primary model
- **Don't address persona depth** — no evidence that brief addenda improve persona adoption on fallback models

## Measuring Impact

After applying, monitor for:

1. **Fewer privacy leaks** in fallback responses (phone numbers, JIDs in visible text)
2. **Fewer unsolicited actions** when GPT handles group chats
3. **More honest tool reporting** (no "voice played" when exec failed)
4. **No degradation** in primary model behavior (check for unnecessary hedging)

## References

- `references/gpt-5.4-failure-modes.md` — Documented GPT-5.4 issues with sources
- `references/cross-model-prompting.md` — OpenAI vs Anthropic prompt engineering differences

## Pairs Well With

- [smart-model-router](https://clawhub.com/globalcaos/smart-model-router) — pick the right model, then Adapter makes sure it behaves
- [agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers) — engineering discipline for multi-model sub-agent pipelines

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._
