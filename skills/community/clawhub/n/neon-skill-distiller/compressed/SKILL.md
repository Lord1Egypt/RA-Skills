---
name: Skill Distiller (Compressed)
version: 0.2.1
description: Same skill compression power in half the context — 975 tokens vs 2,500.
author: Live Neon <lee@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/skill-distiller/compressed
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
  - lightweight
  - openclaw
---

# Skill Distiller (Compressed)

Self-compressed prose variant (~975 tokens, ~90% functionality, LLM-estimated). Full reference: `../SKILL.reference.md`.

## Agent Identity

**Role**: Help users compress verbose skills to reduce context window usage
**Understands**: Skills are verbose for human clarity but costly for context
**Approach**: Identify section types, score importance, remove/shorten low-value sections
**Boundaries**: Preserve functionality, report what was removed, never hide trade-offs
**Tone**: Technical, precise, transparent about trade-offs

**Data handling**: All analysis uses your agent's configured model. No external APIs.

## When to Use

Activate when the user asks:
- "Compress this skill"
- "Make this skill smaller"
- "Distill this skill to X tokens"
- "Reduce skill context usage"

---

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `threshold` | threshold (preserve X%), tokens (fit budget), oneliner |
| `--threshold` | `0.9` | Functionality preservation target (0.0-1.0) |
| `--tokens` | - | Target token count |
| `--provider` | `auto` | ollama, gemini, openai (auto-detects) |
| `--verbose` | `false` | Show section-by-section analysis |
| `--dry-run` | `false` | Analyze without outputting |

*Full options (--model, --debug-stages, --with-ci): see [SKILL.reference.md](../SKILL.reference.md)*

**Threshold = semantic capability, not size ratio.** A 0.9 threshold means 90% of *agent behavior* preserved, not 90% of lines kept. Judge by understanding, not metrics.

---

## Process

### 1. Parse Skill

Parse into sections: Frontmatter, Headers, Code blocks, Lists, Prose.

### 2. Classify Sections

| Type | Importance | Compressible? |
|------|------------|---------------|
| TRIGGER | 1.0 | No |
| CORE_INSTRUCTION | 1.0 | No |
| CONSTRAINT | 0.9 | Partially |
| OUTPUT_FORMAT | 0.8 | Partially |
| EXAMPLE | 0.5 | Yes |
| EXPLANATION | 0.3 | Yes |
| VERBOSE_DETAIL | 0.2 | Yes (first) |

**Protected patterns** (boost to 0.85+): YAML `name`/`description`, Task creation, N-count tracking, Checkpoint/state, BEFORE/AFTER markers.

### 3. Apply Compression

- **Threshold**: Sort by importance, include until target reached
- **Token-target**: Fit budget, summarize if below minimum
- **One-liner**: TRIGGER/ACTION/RESULT format

### 4. Measure Functionality

**Evaluate by semantic understanding, NOT metrics.**

| Wrong | Right |
|-------|-------|
| "60% line reduction is too aggressive" | "Can an agent execute this skill?" |
| "Token ratio exceeds target" | "Are triggers and actions preserved?" |

LLM scores 0-100 based on semantic capability, not line/token ratios. A 50% size reduction can preserve 95% functionality if removed content was verbose/redundant.

### 5. Save Calibration

Append to `.learnings/skill-distiller/calibration.jsonl` with metrics and expected score.

### 6. Output Result

```
Functionality preserved: 90% (uncalibrated - first 5 compressions build baseline)
Tokens: 2000 → 1800 (10% reduction)
Removed: [list], Kept: [list]
[Compressed skill markdown...]
```

---

## Patterns

### Protected (must preserve)

| Pattern | Why |
|---------|-----|
| YAML `name`/`description` | REQUIRED by spec |
| N-count tracking | Observation workflow |
| Task creation | Compaction resilience |

If removed: -10% score penalty, flagged in output.

### Advisory (warn if removed)

Parallel/serial decisions, performance hints, caching guidance. No score penalty.

---

## Calibration

**Storage**: `.learnings/skill-distiller/calibration.jsonl`

| N-count | Meaning |
|---------|---------|
| N < 5 | Uncalibrated (LLM-only estimate) |
| N > 10 | Calibrated (historical CI) |

**Feedback**: `/skill-distiller feedback --id=c1 --actual=85 --outcome="worked"`

---

## Self-Compression

**Guardrails**:
- Require 95% functionality (not 90%)
- Output to SKILL.compressed.md, never overwrite original
- Manual verification required

**Why 0.95**: Capability loss compounds (0.95 x 0.95 = 0.90 at next level).

---

## Error Handling

| Error | Hint |
|-------|------|
| No content | Provide SKILL.md path or pipe via stdin |
| No frontmatter | Add `---` block with `name`/`description` |
| LLM unavailable | Run `ollama serve` or set GEMINI_API_KEY |

---

## Related

| Variant | Tokens | Functionality |
|---------|--------|---------------|
| [skill-distiller](../) (main) | ~400 | ~90% (formula) |
| **compressed** (this) | ~975 | ~90% (prose) |
| [oneliner](../oneliner/) | ~100 | ~70% |

Full reference: [SKILL.reference.md](../SKILL.reference.md) (~2,500 tokens, ~90%)

*Token counts use 4 chars/token heuristic (+/-20%). Functionality scores are LLM-estimated.*
