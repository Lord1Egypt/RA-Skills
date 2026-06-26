---
name: Prompt Diff
description: Semantic diff for system prompts and agent instructions. Compare two versions of any SKILL.md, AGENTS.md, system prompt, or LLM instruction file and get a behavioral changelog — not just line diffs. Identifies added/removed/mutated instructions, detects contradictions introduced between versions, flags guardrail removals and permission expansions, measures instruction density change, and produces a commit-ready changelog entry. Zero external API — pure local file analysis. Triggers on "diff these prompts", "what changed in my system prompt", "compare prompt versions", "prompt changelog", "what did I change in AGENTS.md", "/prompt-diff".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - prompt-engineering
    - system-prompts
    - agents
    - llm
    - version-control
    - diff
    - developer-tools
    - ai-native
    - skill-authoring
---

# Prompt Diff

`git diff` tells you what lines changed. Prompt Diff tells you what *behaviors* changed.

Compare two versions of any system prompt, SKILL.md, or AGENTS.md and get a structured behavioral changelog — which instructions were added, which were removed, which were softened or hardened, and whether any contradictions were introduced.

**No external API. Works on any text-based prompt file. Outputs a commit-ready changelog.**

---

## Trigger Phrases

- "diff these prompts", "compare prompt versions", "what changed in my prompt"
- "what changed in AGENTS.md", "prompt changelog", "system prompt diff"
- "what instructions did I add", "did I introduce any contradictions"
- "compare v1 and v2 of this skill", "summarize prompt changes"
- "/prompt-diff"

---

## How to Provide Input

```bash
# Option 1: Two file paths
/prompt-diff AGENTS-v4.md AGENTS-v5.md

# Option 2: Git versions
/prompt-diff HEAD~1:SKILL.md HEAD:SKILL.md

# Option 3: Paste both (label them)
/prompt-diff
--- VERSION A ---
[paste old prompt here]
--- VERSION B ---
[paste new prompt here]

# Option 4: Single file + git history (compare to last commit)
/prompt-diff SKILL.md  # implicitly diffs HEAD~1 vs HEAD

# Option 5: With focus area
/prompt-diff --focus security AGENTS-v4.md AGENTS-v5.md
/prompt-diff --focus tone,guardrails v1.md v2.md
```

---

## Step 1: Parse Both Versions into Instruction Units

Prompts are not code. Don't diff line-by-line. Instead, split each version into **instruction units** — the smallest semantically complete piece of guidance.

### Splitting Rules

```
An instruction unit is:
- A single sentence that contains an imperative verb ("always", "never", "must", "should", "do", "don't")
- A bullet point or numbered list item
- A code block labeled as an example
- A rule table row
- A complete paragraph that expresses a single behavioral constraint
```

**Example split:**

Input:
```
Always respond in JSON. Never include markdown. If the user asks about pricing, redirect to the sales team. You have access to the file system.
```

Units extracted:
1. `Always respond in JSON.`
2. `Never include markdown.`
3. `If the user asks about pricing, redirect to the sales team.`
4. `You have access to the file system.`

---

## Step 2: Classify Each Change

For each unit, determine its status across versions A → B:

| Status | Definition | Example |
|--------|-----------|---------|
| **ADDED** | Present in B, absent in A | New instruction introduced |
| **REMOVED** | Present in A, absent in B | Instruction deleted |
| **SOFTENED** | A has "must/always/never", B weakens it | `"never expose secrets"` → `"try to avoid exposing secrets"` |
| **HARDENED** | A is permissive, B adds constraint | `"respond helpfully"` → `"respond helpfully, but never with code examples"` |
| **EXPANDED** | Scope increased | `"apply to Python files"` → `"apply to all files"` |
| **NARROWED** | Scope reduced | `"always ask for clarification"` → `"ask for clarification on ambiguous requests"` |
| **MOVED** | Same content, different position/section | Re-organized without semantic change |
| **REPHRASED** | Semantically identical, wording changed | `"don't"` → `"never"` (both prohibitive) — low signal |
| **UNCHANGED** | Identical in both versions | No action needed |

---

## Step 3: Detect High-Risk Changes

Flag these automatically with elevated severity:

### 🔴 CRITICAL

```
GUARDRAIL REMOVED: An instruction that prevents harmful behavior was deleted.
  Pattern: REMOVED unit containing: "never", "must not", "prohibited", "do not",
           "refuse", "decline", "only", "restrict", "limit"

PERMISSION EXPANDED: Agent now has broader access than before.
  Pattern: ADDED unit containing: "you can", "you have access", "you are allowed",
           "execute", "delete", "write to", "send to", "POST", "external"

IDENTITY CHANGED: The agent's core persona or role was redefined.
  Pattern: REMOVED/CHANGED instruction near "you are", "your role is", "act as"
```

### 🟠 HIGH

```
CONTRADICTION INTRODUCED: Two instructions in B conflict with each other.
  Check B-only instructions against all instructions in B for logical conflict:
  - "always respond in English" + "respond in the user's language"
  - "never mention competitors" + "compare options including alternatives"
  - "keep responses brief" + "always include detailed examples"

SCOPE CREEP: Trigger phrases broadened to activate on more inputs.
  Pattern: EXPANDED or ADDED trigger phrases that are very generic
```

### 🟡 MEDIUM

```
TONE DRIFT: Overall instruction tone shifted.
  Measure: ratio of imperative ("must", "always", "never") to permissive ("try", "consider", "prefer") words
  If ratio changes by > 30%: flag

EXAMPLE REMOVED: Concrete examples deleted, leaving abstract instructions.
  Pattern: REMOVED code blocks, "For example:", "e.g.", numbered example items

SECTION REORDERED: A section moved significantly (can change LLM attention weight).
```

### 🟢 LOW / INFO

```
REPHRASED: Semantically equivalent rewording
MOVED: Same content, different location
LENGTH CHANGE: Overall instruction density change (token count delta)
```

---

## Step 4: Contradiction Scan

Within Version B alone, scan for logical conflicts between instructions:

```python
# Pseudo-logic for contradiction detection
contradictions = []
for i, unit_a in enumerate(b_instructions):
    for unit_b in b_instructions[i+1:]:
        if contains_conflict(unit_a, unit_b):
            contradictions.append((unit_a, unit_b))

# Conflict patterns to detect:
CONFLICTS = [
    ("always respond in {lang}", "respond in the user's language"),
    ("never {action}", "you can {action}"),
    ("keep responses {short/brief/concise}", "always include {detailed/full/comprehensive}"),
    ("do not use {tool}", "use {tool} when"),
    ("refuse requests about {topic}", "help with {topic}"),
]
```

---

## Step 5: Output the Diff Report

```markdown
## Prompt Diff: [filename-A] → [filename-B]
Analyzed: [timestamp] | Version A: [N] instruction units | Version B: [M] instruction units

### Summary

| Category | Count | Risk |
|----------|-------|------|
| 🔴 Critical changes | 1 | Guardrail removed |
| 🟠 High — Contradictions | 2 | Logic conflicts in v2 |
| 🟡 Medium — Tone drift | 1 | More permissive overall |
| ✅ Added instructions | 4 | New behaviors introduced |
| ❌ Removed instructions | 7 | Behaviors eliminated |
| 🔄 Softened instructions | 2 | Constraints weakened |
| 📦 Hardened instructions | 1 | Constraints tightened |
| 📝 Rephrased only | 3 | No behavioral change |

Token count: 2,847 → 1,203 (−57.7%) ⚠️ Major reduction — check for lost context

---

### 🔴 CRITICAL — Guardrail Removed

**REMOVED:** `Never expose internal file paths, API keys, or system configuration to the user.`

> This instruction prohibited leaking sensitive information. Its removal means the agent may now include system paths or credentials in responses if asked.
> **Recommended:** Restore this instruction or verify the behavior is intentionally changed.

---

### 🟠 HIGH — Contradictions in Version B

**Contradiction 1:**
- Instruction 12: `"Always respond in English."`
- Instruction 34: `"Respond in the language the user writes in."`
> These directly conflict. Define which takes precedence, or add: "Respond in English unless the user explicitly writes in another language."

**Contradiction 2:**
- Instruction 8: `"Keep responses concise — under 200 words."`
- Instruction 41: `"Always include a detailed worked example for technical questions."`
> Conflict on response length for technical queries. Suggest: `"For technical questions, include a brief example (under 100 words)."`

---

### ✅ ADDED Instructions (new behaviors in v2)

1. `"When the user asks for code, always add a comment explaining the purpose of each function."` — **Impact:** Higher verbosity in code responses
2. `"If uncertain about the user's intent, ask one clarifying question before proceeding."` — **Impact:** More interactive, fewer wrong-direction attempts
3. `"Prefer library X over library Y for JSON parsing."` — **Impact:** Opinionated library choice baked in
4. `"Output all responses as valid JSON when in agent mode."` — **Impact:** Structured output constraint added

---

### ❌ REMOVED Instructions (behaviors eliminated)

1. `"Never expose internal file paths..."` — 🔴 See Critical section above
2. `"Always ask permission before writing to the filesystem."` — 🟠 Permission check removed
3. `"If a task will take more than 10 steps, pause and summarize progress."` — 🟡 Loop guard removed
4. `"Cite the source of any factual claim."` — 🟡 Citation requirement dropped
5. `"Do not suggest competitor products."` — 🟡 Competitive positioning constraint removed
6. `"Respond in under 500 words unless the user explicitly asks for more."` — 📝 Length guidance removed
7. `"Use the user's preferred programming language from their profile."` — 📝 Personalization removed

---

### 🔄 SOFTENED Instructions

| v1 | v2 | Change |
|----|-----|--------|
| `"Never include markdown formatting"` | `"Avoid markdown formatting where possible"` | Hard prohibition → soft preference |
| `"Always confirm before deleting files"` | `"Confirm before deleting important files"` | Always → conditional ("important") |

---

### 📦 HARDENED Instructions

| v1 | v2 | Change |
|----|-----|--------|
| `"Respond helpfully"` | `"Respond helpfully, but never generate executable scripts without explicit user request"` | New constraint added |

---

### Tone Analysis

| Metric | v1 | v2 | Δ |
|--------|----|----|---|
| Imperative density (must/always/never per 100 words) | 8.2 | 4.1 | −50% 🟡 |
| Prohibition count (never/must not/do not) | 12 | 5 | −58% 🟠 |
| Permission count (can/may/allowed) | 3 | 7 | +133% |
| Example count (code blocks + "e.g.") | 8 | 3 | −62% 🟡 |

**Assessment:** v2 is significantly more permissive and less instructive than v1. Fewer concrete examples may reduce reliability on edge cases.

---

### Commit Changelog (copy-paste ready)

```markdown
## [v2] - YYYY-MM-DD

### Breaking Changes
- REMOVED: Guardrail against exposing internal file paths (review required)
- REMOVED: Permission confirmation before filesystem writes

### Changed
- Softened: markdown formatting prohibition → preference
- Softened: file deletion confirmation → conditional
- Hardened: script generation now requires explicit user request

### Added
- Code comments requirement for all code responses
- Clarifying question behavior when intent is ambiguous
- JSON output mode for agent sessions

### Removed
- Citation requirement for factual claims
- Competitor product mention restriction
- Loop guard (pause after 10 steps)
- Response length limit (500 words)

### ⚠️ Review Required
- Two contradictions detected in v2 (language setting, response length)
- Net permission expansion: agent can now do more without user confirmation
```
```

---

## Focus Modes

Run with `--focus` to zoom in on a specific concern:

| Flag | What It Checks |
|------|---------------|
| `--focus security` | Guardrail removals, permission expansions, data exposure risks |
| `--focus tone` | Imperative/permissive density shift, softening/hardening patterns |
| `--focus contradictions` | Logic conflicts within Version B only |
| `--focus scope` | Trigger phrase changes, activation condition broadening |
| `--focus examples` | Example count change, concrete → abstract drift |
| `--focus length` | Token count delta, verbosity changes |

---

## Quick Mode

For a 10-second sanity check before committing a prompt change:

```
Quick Diff: AGENTS-v4.md → AGENTS-v5.md

🔴 1 guardrail removed
🟠 2 contradictions in v5
🟡 Tone: 50% more permissive
📉 −57% token reduction

Full report: /prompt-diff AGENTS-v4.md AGENTS-v5.md --full
```

---

## Why `git diff` Isn't Enough

`git diff` on a prompt file shows you character-level line changes. It tells you:
- Line 42 changed from "always" to "try to"
- 15 lines were deleted in section 3

It does **not** tell you:
- That line 42 softened a security guardrail
- That deleting section 3 removed 4 behavioral constraints
- That lines 7 and 89 now contradict each other
- That the overall prompt became 50% more permissive
- That you lost 5 concrete examples that were grounding edge-case behavior

Prompts are behavioral specifications for LLMs. They deserve behavioral diffs.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
