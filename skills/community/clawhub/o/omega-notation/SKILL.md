---
name: omega-notation
description: "Structured output compression for AI agents. Dramatically reduces token cost on structured data (evals, decisions, routing, policies, media summaries). Designed for machine-to-machine agent communication, not prose."
version: "1.0.1"
author: "Shadow Rose"
tags: [compression, tokens, cost-reduction, structured-output, agent-communication]
---

# Ω Notation — Token Compression for AI Agents

## What It Does

Compresses structured agent outputs into ultra-dense shorthand that other agents can parse. Designed for machine-to-machine communication where every token costs money.

## Compression Performance

| Data Type | Reduction | Notes |
|-----------|-----------|-------|
| JSON evals/decisions | ~95-98% | Highest gains — format-heavy, payload-light |
| Routing/dispatch | ~90-95% | Repetitive structure compresses well |
| Policy rules | ~85-90% | Conditional logic has moderate density |
| Media summaries | ~80-85% | Mixed structure + free text |
| Semi-structured logs | ~60-70% | Less redundant format to strip |
| Conversational text | ~30-40% | High semantic density, low format redundancy |

**Key insight:** Compression scales with how much of the original is *format* vs *meaning*. Structured data is mostly format (brackets, keys, boilerplate). Conversation is mostly meaning. Omega Notation strips format — it doesn't compress meaning.

## When To Use

- Agent-to-agent structured messages (evals, routing, decisions)
- High-volume pipelines where token cost matters (batch processing, multi-agent orchestration)
- Decision crystallization (fitness scores, deltas, confidence)
- Policy enforcement outputs
- Media/video summary digests
- Any structured data flowing between AI systems

## When NOT To Use

- Conversational replies to humans
- Prose, documentation, or creative writing
- Anything where human readability matters
- As a global default for all outputs (will break conversational ability)
- Free-form text with no repeating structure

## Format

Every Ω message starts with a header:

```
!omega v1 dict=auto
```

### Supported Types

| Prefix | Type | Example |
|--------|------|---------|
| `e.d` | Eval digest | `e.d {c:0.95 d:proceed} [cat:finance]` |
| `d.c` | Decision crystallize | `d.c "task-name" {fit:0.98} Δfit:+0.03` |
| `r.d` | Route dispatch | `r.d "handler" {to:opus pri:high}` |
| `p.e` | Policy enforce | `p.e "safety" {if:conf<0.5 then:escalate}` |
| `t.es` | Tier escalate | `t.es {from:1 to:2 reason:"low-conf"}` |
| `m.c` | Media compress | `m.c "vid-1" {h:phash:abc len:142 cap:"""summary"""}` |

### Tags

Append tags in brackets: `[cat:finance]` `[pri:high]` `[src:apex]`

### Deltas

Use Δ prefix for changes: `Δfit:+0.03` `Δconf:-0.1`

### Multi-line

Multiple operations in one message:

```
!omega v1 dict=auto
e.d {c:0.92 d:hold} [cat:trading]
d.c "btc-position" {fit:0.87} Δfit:-0.05
t.es {from:1 to:2 reason:"regime-shift"}
```

## Round-Trip Integrity

Omega Notation includes a TypeScript serializer/deserializer with full round-trip verification. Structured data compressed → decompressed returns identical objects. The `test()` function validates this automatically.

## Usage

When you want structured output compressed, include Ω Notation format in your request:

```
Give me the eval results in Ω Notation format.
```

The agent will use the prefix syntax (`e.d`, `d.c`, `r.d`, etc.) for that response. Conversational replies stay normal — Ω Notation is invoked per-request, not globally.

## Dictionary System

- `dict=auto` — agent builds shorthand mappings over time within a session
- `dict=none` — no dictionary, all explicit
- Custom: `dict={proceed:p, escalate:e, hold:h}` — define upfront

## Technical Details

- TypeScript implementation with serialize/deserialize functions
- No external dependencies
- Built-in round-trip test
- Extensible type system — add new prefixes for domain-specific structured data

## Modes

### `mode=struct` (default, shipped)
Structured data compression. 90-98% reduction. Round-trip verified. Use this.

### `mode=context` (v2, coming soon)
Prose/context compression using law-derived predictive encoding. Based on the Law of Non-Closure applied to LLM-to-LLM communication — the decoder's knowledge IS the codebook, so only surprise content needs transmitting. Theoretical ceiling: ~70-80% reduction on conversational text. Not yet implemented.

## Theoretical Basis

Omega Notation exploits the fact that structured data is mostly *format* (brackets, keys, whitespace, boilerplate) with small *payloads* (values, scores, names). Stripping predictable format while preserving payload achieves high compression on structured types. Conversational text has the inverse ratio — mostly payload, little format — which is why compression drops for prose.

v2 will use a fundamentally different approach for prose: predictive compression where the LLM's training acts as a shared codebook between encoder and decoder. Only tokens the decoder can't predict need transmitting. The compression floor is H(message | decoder_knowledge) — a result derived from information theory and thermodynamic law.
