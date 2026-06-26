---
name: Skill Distiller
version: 0.2.1
description: Fit more skills in your context window — compress without losing what matters.
author: Live Neon <lee@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/skill-distiller
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
  - openclaw
---

# Skill Distiller

Compress verbose skills to reduce context window usage. This skill is self-compressed using formula notation (~400 tokens, ~90% functionality, LLM-estimated). Full reference version: `SKILL.reference.md`.

> **Note**: This skill uses formula notation — the LLM executes these operations directly.
> You don't need to understand the math. For prose explanation, see [SKILL.reference.md](./SKILL.reference.md).

## Legend

```
S = {TRIGGER, CORE, CONSTRAINT, OUTPUT, EXAMPLE, EDGE, EXPLAIN, VERBOSE}
I(s) ∈ [0,1]        # importance score
P = {yaml.name, yaml.desc, N-count, task-create, checkpoint, BEFORE/AFTER}  # protected
θ ∈ [0,1]           # threshold (default 0.9)
n ∈ ℕ               # target tokens
```

## Operations

### compress(skill, θ)
```
∀s ∈ skill: type(s) → S, score(s) → I(s)
s ∈ P ⇒ I(s) := max(I(s), 0.85)
keep = {s | I(s) ≥ θ ∨ s ∈ P}
output = (skill[keep], Σ I(keep)/|S|, |skill| - |keep|)
# Score divides by |S| (8 types), not |keep| — rewards diverse section coverage
```

### compress_tokens(skill, n)
```
min_tokens = |{s | type(s) ∈ {TRIGGER, CORE}}|
n < min_tokens ⇒ summarize(skill) → n
n ≥ min_tokens ⇒ compress(skill, θ) where |output| ≤ n
```

### oneliner(skill)
```
output = "TRIGGER: " + extract(skill, TRIGGER) +
         "\nACTION: " + extract(skill, CORE) +
         "\nRESULT: " + extract(skill, OUTPUT)
```

### recomp(examples, coverage_target=0.8)
```
scored = [(e, pattern_coverage(e), uniqueness(e)) | e ∈ examples]
selected = top(scored, n=2, by=coverage × uniqueness)
coverage(selected) ≥ 0.8 ⇒ phase1
  output = selected ∪ {trigger(e) → result(e) | e ∈ examples \ selected}
coverage(selected) < 0.8 ⇒ phase2
  output = synthesize(examples) → single_example
```

### token_score(section) — for type ∈ {EXAMPLE, EDGE, EXPLAIN, VERBOSE}
```
∀phrase ∈ section:
  self_info(phrase) = -log(P(phrase|context))
  high_info ⇒ KEEP, low_info ⇒ PRUNE
prune while preserving sentence structure
>50% low_info ⇒ remove entire section
```

## Symbols (MetaGlyph)

| Symbol | Meaning |
|--------|---------|
| `→` | results in, maps to |
| `⇒` | implies, therefore |
| `∈` | element of, in |
| `∀` | for all |
| `¬` | not |
| `∧` | and |
| `∨` | or |
| `:=` | assign |

## Invocation

```
/skill-distiller path --threshold=0.9  →  compress(skill, 0.9)
/skill-distiller path --tokens=500     →  compress_tokens(skill, 500)
/skill-distiller path --mode=oneliner  →  oneliner(skill)
```

## Errors

| Condition | Response |
|-----------|----------|
| `skill = ∅` | "No content" |
| `¬∃ yaml.name` | "Add frontmatter" |
| `n < min_tokens` | "Summarizing..." |

---

## Variants

| Variant | Tokens | Functionality |
|---------|--------|---------------|
| **main** (this) | ~400 | ~90% (formula) |
| [compressed](./compressed/) | ~975 | ~90% (prose) |
| [oneliner](./oneliner/) | ~100 | ~70% |

Full reference: [SKILL.reference.md](./SKILL.reference.md) (~2,500 tokens, ~90%)

*Token counts use 4 chars/token heuristic (+/-20%). Functionality scores are LLM-estimated.*
