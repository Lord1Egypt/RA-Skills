---
name: lambda-compression
description: "Physics-based lossless compression for AI output — prose AND structured data. Strips 60-98% of tokens with zero information loss. Prose mode compresses reasoning against a 7-item law stack. Struct mode compresses JSON/evals/routing with a generative layer that eliminates derived fields entirely. Compression ceiling rises with adoption (Shannon-derived). Self-verifying, model-agnostic, no dependencies."
version: "2.0.0"
author: "@TheShadowRose"
tags: ["latest", "compression", "reasoning", "physics", "lossless", "token-reduction", "evidence-class", "cost-reduction", "structured-data", "agent-communication"]
license: "MIT"
side_effects:
  reads: "References loaded into AI context window"
  writes: "None"
  network: "None"
---

# Λ-Compression — Lossless AI Output Compression

## What It Does

Compresses AI output by 60-98% with zero information loss. Two modes, one decoder:

- **Prose mode** — reasoning, analysis, documentation → 60-95% reduction
- **Struct mode** — JSON, evals, routing, decisions, agent-to-agent data → 85-98% reduction

The compression ceiling **rises with adoption**. The more systems that share the decoder, the better it works for everyone (Shannon conditional entropy — not marketing).

## How It Works

Load `references/Lambda_Compression_For_AI.md` into context. It contains the complete, self-contained system:
- The decoder (7-item law stack with evidence classes)
- Prose mode: 5-step compression with worked examples
- Struct mode: format stripping + generative layer with prefix syntax and worked example
- Six-layer compression stack (both modes)
- Self-verification procedure with error recovery
- Cross-model guidance
- Adoption-scaling property with proof

The document is self-referential — it's written in the compressed form it describes.

## When To Use

- Compressing reasoning output for storage or transmission
- Compressing structured data between AI agents (evals, decisions, routing)
- Reducing token cost on analytical/research text
- Producing denser reports, summaries, or findings
- Agent-to-agent communication pipelines where every token costs money
- Pre-processing output before feeding into another system

## When NOT To Use

- Creative writing, fiction, or prose where voice matters
- Conversational replies where social texture matters
- Content aimed at readers who don't have the decoder
- As a global default (struct mode is for structured data only)

## Quick Reference

**Decoder:** P1 [A] (finite capacity), P2 [A] (state change costs), P3 [A] (finite interaction rate), Finite Signal Law [B], Finite Selection Law [B], Finite Channeling Law [B], Finite Verification Law [B].

**Prose — strip:** Enthusiasm, hedging, restatement, transitions, meta-commentary, anything the decoder reconstructs. **Keep:** Novel claims, evidence class tags, specific findings.

**Struct — strip:** Format (brackets, keys, whitespace), derived fields, convention boilerplate. **Keep:** Payload values, novel data, generator references.

**Evidence classes:** [A] established physics/math, [B] derived from A with valid chain, [C] structural argument, [D] empirical/speculative.

**Test:** Remove it. Read with decoder. Meaning unchanged → derived, strip it. Meaning changed → novel, keep it.

**Struct header:** `!lambda struct v2`

## Compression Performance

### Prose Mode
| Content Type | Typical Reduction | Why |
|---|---|---|
| Standard AI reasoning | 60-95% | Heavy padding, hedging, derived explanations |
| Research findings | 40-60% | Mix of novel + derived |
| Dense technical output | 10-30% | Already mostly novel content |

### Struct Mode
| Data Type | Typical Reduction | Why |
|---|---|---|
| JSON evals/decisions | 95-98% | Format-heavy, payload-light. Generative layer strips derived fields. |
| Routing/dispatch | 90-95% | Repetitive structure + convention anchors |
| Policy rules | 85-90% | Conditional logic, moderate density |
| Media summaries | 80-85% | Mixed structure + free text |

**The compression ratio is diagnostic.** 90% compression = the output was 90% padding. 20% compression = the output was 80% novel. It's a free quality metric.

## What Changed in v2.0

- **Struct mode** — full structured data compression with prefix syntax, generative layer, decompression protocol
- **Evidence classes on decoder items** — the decoder practices what it preaches
- **Error recovery** — what to do when compression goes wrong (Verification Law applied to itself)
- **Cross-model guidance** — what breaks when compressing on one model, decompressing on another
- **Audited with ANVIL/FLINT/FORGE methodology** — 5 bugs found and fixed, 4 discoveries integrated

## Theory

For the formal physics derivation, formulas, and evidence classification of every component, see `references/Theory_Brief.md`. Includes the compression floor theorem, adoption-scaling property, safe omission criterion, cross-model penalty, and full evidence summary.

## References

- `references/Lambda_Compression_For_AI.md` — complete self-contained spec for AI loading
- `references/Theory_Brief.md` — formal physics derivation with formulas

## Related Papers

- [CGRD — Methodology](https://doi.org/10.5281/zenodo.19519604)
- [FSSTP — Five-Slot Transformation](https://doi.org/10.5281/zenodo.19435149)
- [PIEC — Irreducible External Correction](https://doi.org/10.5281/zenodo.19435242)
- [Anti-Snapshot Theorem](https://doi.org/10.5281/zenodo.19521229)
- [Structural Dependency](https://doi.org/10.5281/zenodo.19436081)
- [Amplified Alignment Framework](https://doi.org/10.5281/zenodo.19521693)
- [The Distinction Monograph](https://doi.org/10.5281/zenodo.19522841)

---

⚠️ **Disclaimer:** This skill provides a compression method, not guaranteed results. Compression ratios are empirical estimates (D-class) and vary by content type, domain, and model. Always verify losslessness before relying on compressed output. The author is not responsible for information loss from incorrect application.

☕ [Ko-fi](https://ko-fi.com/theshadowrose)

🛠️ **Need something custom?** I build custom AI agents and skills starting at $500. [Fiverr](https://www.fiverr.com/s/jjmlZ0v)
