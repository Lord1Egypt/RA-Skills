---
name: Skill Distiller (One-Liner)
version: 0.2.1
description: Skill compression reminder in 100 tokens — just trigger, action, result.
author: Live Neon <lee@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/skill-distiller/oneliner
repository: live-neon/skills
license: MIT
user-invocable: true
disable-model-invocation: true
emoji: "\U0001F5DC\uFE0F"
tags:
  - compression
  - skills
  - optimization
  - context-window
  - token-reduction
  - quick-reference
  - minimal
  - openclaw
---

# Skill Distiller (One-Liner)

Minimal reference variant (~100 tokens, ~70% functionality, LLM-estimated). Full reference: `../SKILL.reference.md`.

**TRIGGER**: User asks to compress, distill, or reduce a skill's context usage

**ACTION**: Parse skill into sections (TRIGGER/INSTRUCTION/EXAMPLE/etc), score importance via LLM, remove low-value sections while preserving protected patterns (YAML name/description, N-count tracking, task creation)

**RESULT**: Compressed skill markdown with functionality score (0-100%), token reduction stats, and list of removed/kept sections

---

## Related

| Variant | Tokens | Functionality |
|---------|--------|---------------|
| [skill-distiller](../) (main) | ~400 | ~90% (formula) |
| [compressed](../compressed/) | ~975 | ~90% (prose) |
| **oneliner** (this) | ~100 | ~70% |

Full reference: [SKILL.reference.md](../SKILL.reference.md) (~2,500 tokens, ~90%)

*Functionality scores are LLM-estimated.*
