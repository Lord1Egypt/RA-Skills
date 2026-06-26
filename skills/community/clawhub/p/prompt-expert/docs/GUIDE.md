# Prompt Expert — Reference Guide

Merged reference (principles, techniques, troubleshooting, checklists). For the **prompt-expert** skill.

## Core principles

1. **Clarity** — Explicit tasks; concrete examples; logical hierarchy.  
2. **Conciseness** — Respect context limits; remove redundancy; progressive disclosure.  
3. **Degrees of freedom** — Clear constraints, format, scope; balance control vs. reasoning room.

## Advanced techniques (short)

| Technique | Use when |
|-----------|----------|
| **Chain-of-thought** | Multi-step reasoning; need transparent logic. |
| **Few-shot** | Shape behavior with 1–N labeled examples. |
| **XML / structure** | Parsing, sections, repeatable layouts. |
| **Role-based** | Domain tone, boundaries, responsibilities. |
| **Prefill** | Lock first lines for format/tone. |
| **Chaining** | Pipeline: extract → analyze → summarize. |
| **Context** | Progressive disclosure; hierarchy; only necessary tokens. |
| **Multimodal** | Vision: specify what to extract; files: type + structure; embeddings: similarity tasks. |

## Custom instructions & system prompts

- Role, tone, constraints, scope, escalation (when to ask).  
- Skill naming: lowercase hyphenated (e.g. `prompt-expert`); description: capabilities + use cases, avoid vague “helps with”.

## Skill layout (recommended)

```
skill-name/
├── SKILL.md       # entry + YAML + role
├── skill.json     # optional manifest
├── docs/          # this guide
└── examples/      # templates
```

## Evaluation & testing

- Success criteria: measurable, testable, realistic.  
- Cases: happy path, edge, error, stress.  
- Failure analysis → refine; regression-test after changes.

## Anti-patterns

- Vague goals; contradictory rules; over-constraining; prompts that invite fabrication; context leakage; injection-prone patterns.

## Troubleshooting (quick)

| Symptom | Levers |
|---------|--------|
| Inconsistent output | Format spec + examples + XML; role prompt. |
| Hallucination | Grounding, caveats, confidence, “what you don’t know.” |
| Too vague | Context, objective, success criteria, exemplar outputs. |
| Wrong length | Word/sentence bounds; scope. |
| Wrong format | Schema, JSON/XML example, field list. |
| Refusal | Legitimate framing; creative/educational context. |
| Prompt too long | Summaries, links to refs, fewer shots. |
| Brittle | Variables not literals; multiple input shapes; errors specified. |

**Debug loop:** reproduce → inspect prompt (goal, context, format) → hypothesis → edit → multi-input validation → document.

## YAML frontmatter (skills)

```yaml
---
name: skill-name
description: Clear, concise description (max ~1024 chars)
---
```

## Token budget (rule of thumb)

- Metadata: ~100–200 tokens; main instructions: ~500–1000; each deep reference: ~1k–5k.

## Checklist (skills)

**Quality:** clear name; short description; structure; progressive disclosure; terminology; no stale dates.  
**Content:** use cases; examples; edge cases; limitations; troubleshooting pointer.  
**Testing:** cases; criteria; edge/error handling; regression.  
**Docs:** SKILL links here; examples; integration notes.
