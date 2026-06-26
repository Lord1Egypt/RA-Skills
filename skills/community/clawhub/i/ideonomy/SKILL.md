---
name: ideonomy
version: "0.3.1"
description: Structured creative reasoning through ideonomic lenses. Use when stuck on a problem, need fresh perspectives, want to think more creatively or systematically, or need to explore a problem from multiple angles. Based on Patrick Gunkel's "science of ideas" — systematic combinatorial thinking across 28 reasoning divisions.
---

# Ideonomy Engine

Structured creative reasoning using ideonomic divisions as thinking lenses.

## Installation

```bash
npm install -g @clawdactual/ideonomy-engine
```

Verify with:

```bash
ideonomy --help
```

## Quick Start

```bash
# Basic reasoning (auto-selects profile based on problem keywords)
ideonomy reason "Your problem statement here"

# Concise mode (just core questions, one per lens)
ideonomy reason --concise "Your problem statement here"

# JSON output (structured, machine-parseable)
ideonomy reason --json "Your problem statement here"
```

## Profiles

Force a reasoning style with `--profile`:

| Profile | Best For |
|---------|----------|
| `technical` | Engineering, architecture, debugging, system design |
| `creative` | Brainstorming, ideation, novel solutions |
| `strategic` | Planning, decisions, competitive analysis, long-term thinking |
| `ethical` | Moral dilemmas, values conflicts, right vs wrong |
| `diagnostic` | Debugging, root cause analysis, troubleshooting |
| `interpersonal` | Relationships, communication, team dynamics |
| `philosophical` | Deep questions about meaning, existence, knowledge |
| `general` | Balanced default covering universally useful divisions |

Auto-selection scores problem text against profile keywords. Override with `--profile <id>`.

## Options

- `--profile <id>` — force a reasoning profile
- `--divisions <THEME1,THEME2,...>` — cherry-pick specific divisions (e.g. `ANALOGIES,CAUSES,LIMITS`)
- `--lenses <n>` — limit number of lenses returned
- `--concise` — core questions only (minimal output)
- `--json` — structured JSON output

## Other Commands

```bash
ideonomy profiles          # list all profiles
ideonomy divisions         # list all 28 reasoning divisions
ideonomy division ANALOGIES # detail for one division
```

## How to Use the Output

The engine produces **structured prompts, not answers**. For each lens:
1. **Core question** — the essential question this division asks about your problem
2. **Guiding questions** — specific angles to explore
3. **Cross-domain sparks** — unexpected domain pairings to stimulate lateral thinking
4. **Conceptual palette** — organon items for combinatorial inspiration

**Best approach:** Run the engine, then think through each lens yourself. The guiding questions are the highest-value part. The cross-domain sparks work ~30% of the time but produce genuinely novel ideas when they hit.

## When to Use

- Stuck on a problem and default thinking isn't working
- Need to systematically explore angles you'd normally miss
- Want to challenge assumptions (use OPPOSITES, INVERSIONS, FIRST PRINCIPLES)
- Debugging something subtle (use `--profile diagnostic`)
- Brainstorming and want structured creativity (use `--profile creative`)
- Making a strategic decision with trade-offs (use `--profile strategic`)
