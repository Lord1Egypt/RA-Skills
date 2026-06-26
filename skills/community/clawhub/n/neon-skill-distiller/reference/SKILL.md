---
name: Skill Distiller (Reference)
version: 0.2.1
description: Complete skill compression documentation — all options, modes, and calibration details (~2,500 tokens).
author: Live Neon <lee@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/skill-distiller/reference
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
  - reference
  - documentation
  - openclaw
---

# Skill Distiller (Reference)

Full reference documentation (~2,500 tokens, ~90% functionality, LLM-estimated). This is the canonical source for all compressed variants.

> **Note**: This reference document intentionally exceeds the 300-line MCE guideline.
> As the canonical source for all compressed variants, comprehensiveness is prioritized
> over brevity. For compact variants, see the main [SKILL.md](../SKILL.md) (~400 tokens, formula)
> or [compressed](../compressed/SKILL.md) (~975 tokens, prose).

## Agent Identity

**Role**: Help users compress verbose skills to reduce context window usage
**Understands**: Skills are verbose for human clarity but costly for context; compression is a trade-off
**Approach**: Identify section types, score importance, remove/shorten low-value sections
**Boundaries**: Preserve functionality, report what was removed, never hide trade-offs
**Tone**: Technical, precise, transparent about trade-offs

**Data handling**: This skill operates within your agent's trust boundary. All analysis uses your agent's configured model. No external APIs beyond your agent's LLM provider.

## When to Use

Activate this skill when the user asks:
- "Compress this skill"
- "Make this skill smaller"
- "Distill this skill to X tokens"
- "What can I remove from this skill?"
- "Reduce skill context usage"

---

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `threshold` | Compression mode: threshold, tokens, oneliner |
| `--threshold` | `0.9` | Functionality preservation target (0.0-1.0) |
| `--tokens` | - | Target token count (for tokens mode) |
| `--provider` | `auto` | LLM provider: auto, ollama, gemini, openai |
| `--model` | - | Specific model (e.g., llama3.2, gemini-2.0-flash) |
| `--verbose` | `false` | Show section-by-section analysis |
| `--dry-run` | `false` | Analyze without outputting compressed skill |
| `--debug-stages` | `false` | Show intermediate stage outputs |

**Provider auto-detection** (in order):
1. Check `ollama` availability via `ollama list`
2. Check `GEMINI_API_KEY` environment variable
3. Check `OPENAI_API_KEY` environment variable
4. Error if none available

---

## Process

### 1. Provider Detection

```
IF ollama available → use ollama (local, fast)
ELIF GEMINI_API_KEY set → use gemini
ELIF OPENAI_API_KEY set → use openai
ELSE → Error: "No LLM provider available. Run 'ollama serve' for local inference, or set GEMINI_API_KEY for cloud."
```

### 2. Parse Skill

Parse input skill into sections:
- **Frontmatter** (YAML header with name, description)
- **Headers** (##, ### sections)
- **Code blocks** (examples, output format)
- **Lists** (triggers, constraints)
- **Prose** (explanations)

### 3. Classify Sections

Classify each section using LLM:

| Type | Importance | Compressible? |
|------|------------|---------------|
| TRIGGER | 1.0 (required) | No |
| CORE_INSTRUCTION | 1.0 (required) | No |
| CONSTRAINT | 0.9 | Partially |
| OUTPUT_FORMAT | 0.8 | Partially |
| ADVISORY_PATTERN | 0.7 | Yes, with warning |
| EXAMPLE | 0.5 | Yes (reduce count) |
| EDGE_CASE | 0.4 | Yes (summarize) |
| EXPLANATION | 0.3 | Yes (remove) |
| VERBOSE_DETAIL | 0.2 | Yes (remove first) |

**Protected patterns** (boost to 0.85+):
- YAML `name`/`description` (REQUIRED BY SPEC)
- Task creation references
- N-count tracking (N=1, N=2, N≥3)
- Checkpoint/state recovery
- BEFORE/AFTER markers

### 3.5. Token-Level Importance (LLMLingua/Selective Context)

For compressible sections (EXAMPLE, EDGE_CASE, EXPLANATION, VERBOSE_DETAIL), apply token-level scoring based on self-information theory:

**Principle:** `self_info(token) = -log(P(token|context))`
- HIGH self-information = surprising/important → KEEP
- LOW self-information = predictable/removable → PRUNE

**Scoring Prompt:**
```
Analyze this section for compression. Classify phrases as:
- ESSENTIAL: Specific values, unique terms, key constraints, surprising info
- REDUNDANT: Could be inferred, restates earlier content, filler words

Section type: {type}
Content: {content}

Return JSON: {"essential": [...], "redundant": [...], "compression_potential": 0.0-1.0}
```

**Pruning Rules:**
1. Never prune ESSENTIAL tokens
2. Remove REDUNDANT phrases while preserving sentence structure
3. If >50% is REDUNDANT, consider removing entire section
4. Preserve specific values (numbers, thresholds, error codes)

**Example:**
```
Input:  "The system will then proceed to process the input data and return the results"
Output: "process input data → return results"
Removed: "The system will then proceed to", "and"
```

### 4. Apply Compression

**All modes use MetaGlyph native symbols** (see §Symbol Reference below):
- Replace "results in" → `→`
- Replace "implies" → `⇒`
- Replace "for all" → `∀`
- Replace "not" → `¬`

**Threshold Mode** (default):
1. Sort sections by importance (descending)
2. Include sections until functionality target reached
3. Apply symbol substitutions
4. Generate compressed markdown

**Token-Target Mode**:
1. Calculate minimum tokens (triggers + core)
2. If target < minimum: attempt LLM summarization
3. Add sections by importance until target
4. Apply symbol substitutions

**One-Liner Mode**:
1. Extract trigger conditions
2. Extract core action
3. Extract expected result
4. Format as 3-line summary with symbols

### 4.1. Example Compression (RECOMP)

For EXAMPLE sections, use extractive + abstractive compression:

**Phase 1: Extractive Selection** (preferred)
1. Score each example for pattern coverage, uniqueness, clarity
2. Select top 1-2 examples (keep full detail)
3. Compress remaining examples to one-liners (don't discard)
4. If coverage ≥ 0.8 → use selected + one-liners

**Phase 1.5: One-Liner Compression** (for non-selected examples)
Instead of discarding, compress to: `{trigger} → {result}`
- Use MetaGlyph symbols
- Preserves coverage, reduces tokens
- Group under "### One-liners:" heading

**Output structure:**
```markdown
### Full (selected):
[Detailed example with steps...]

### One-liners (compressed):
- `--mode=tokens` → hard token limit
- `--verbose` → section-by-section analysis
```

**Phase 2: Abstractive Fallback** (if extractive + one-liners < 0.8)
1. Generate summary example combining key patterns
2. Format: `{generalized_pattern} → {expected_result}`
3. Preserve specific values where critical

**Selection Prompt:**
```
Select the 1-2 BEST examples that cover the most patterns with minimum redundancy.

Examples:
{numbered_list}

Return JSON: {
  "selected": [indices],
  "coverage": 0.0-1.0,
  "rationale": "..."
}
```

**Synthesis Prompt** (if coverage < 0.8):
```
Compress these examples into 1-2 summary examples.
Preserve: specific values, key patterns, expected outcomes.
Format: "When X → Do Y → Expect Z"

{examples}
```

**Output shows:** `Examples: 5 → 2 full + 3 one-liners (extractive)` or `Examples: 5 → 1 (abstractive)`

### 5. Measure Functionality

**Evaluate by semantic understanding, NOT metrics.**

| Wrong (Metrics) | Right (Semantic) |
|-----------------|------------------|
| "60% line reduction is too aggressive" | "Can an agent still execute this skill?" |
| "Token count exceeds target" | "Are all triggers and actions preserved?" |
| "Ratio doesn't match threshold" | "Would an agent behave the same way?" |

LLM evaluates preservation by asking:
- Can all original triggers still activate?
- Are all core actions still specified?
- Are critical constraints preserved?
- Would an agent behave the same way?

**Score 0-100** reflects semantic capability preservation, not line/token ratios. A skill compressed to 40% of original size can still preserve 95% functionality if the removed content was verbose explanation, redundant examples, or non-essential formatting.

### 6. Save Calibration

After compression, save entry to `.learnings/skill-distiller/calibration.jsonl`:

```json
{
  "id": "c[N]",
  "timestamp": "[ISO 8601]",
  "skill": "[skill name from frontmatter]",
  "mode": "[threshold|tokens|oneliner]",
  "threshold": 0.9,
  "input_tokens": 1800,
  "output_tokens": 1100,
  "reduction_pct": 39,
  "sections_total": 14,
  "sections_kept": 9,
  "sections_removed": 5,
  "classification_confidence_mean": 0.90,
  "functionality_score": 90,
  "protected_patterns_found": ["n-count"],
  "protected_patterns_preserved": ["n-count"],
  "advisory_patterns_found": [],
  "advisory_patterns_removed": [],
  "expected": {"functionality": 90},
  "actual": null
}
```

**File rotation**: If entries > 1000, truncate oldest 100 before appending.

### 7. Output Result

Return compressed skill with metadata.

---

## Output

### Standard Output

```
Functionality preserved: 90% (uncalibrated - first 5 compressions build baseline)
Tokens: 2000 → 1800 (10% reduction)
Classification confidence: 0.87 (mean across sections)

Removed: 3 examples, 2 edge cases
Kept: all triggers, core instructions, constraints

[Compressed skill markdown follows...]
```

### Verbose Output (`--verbose`)

```
Section Analysis:
  ## When to Use: TRIGGER (1.0, confidence: 0.95) → KEPT
  ## Process: CORE_INSTRUCTION (1.0, confidence: 0.92) → KEPT
  ## Examples: EXAMPLE (0.5, confidence: 0.88) → RECOMP
    └─ Examples: 5 → 2 full + 3 one-liners (coverage: 0.95)
  ## Edge Cases: EDGE_CASE (0.4, confidence: 0.85) → SUMMARIZED
  ## Technical Details: VERBOSE_DETAIL (0.2) → TOKEN-SCORED
    └─ Tokens: 150 → 45 (redundant phrases removed)

Token-level analysis:
  VERBOSE_DETAIL sections: 3 analyzed, 67% average compression
  Phrases removed: "The system will then", "proceed to", "in order to"

RECOMP example analysis:
  Original examples: 5
  Full (selected): [0, 4] (basic usage, error handling)
  One-liners: [1, 2, 3] (threshold, tokens, verbose options)
  Coverage: 0.95 (full + one-liners)
  Mode: extractive

Protected patterns found: none
Advisory patterns found: parallel-decision → removed (no score penalty)

[Compressed skill markdown follows...]
```

### One-Liner Output

```
TRIGGER: [activation conditions]
ACTION: [core behavior]
RESULT: [expected output]
```

**Example with MetaGlyph symbols**:
```
TRIGGER: user asks "compress skill" ∨ "distill" ∨ "reduce context"
ACTION: parse → classify sections → score importance → ¬low-value → output
RESULT: compressed skill ∧ functionality% ∧ token reduction stats
```

---

## Compression Modes

### Mode 1: Threshold (Default)

Preserve X% of functionality, compress as much as possible.

```bash
/skill-distiller path/to/skill.md --threshold=0.9
```

**Understanding thresholds**: The threshold (0.9 = 90%) refers to **semantic functionality**, not token/line ratios.

| Threshold | Meaning | NOT |
|-----------|---------|-----|
| 0.95 | 95% of *capabilities* preserved | 95% of *lines* kept |
| 0.90 | 90% of *semantic function* | 90% of *tokens* |
| 0.80 | 80% of *agent behavior* | 80% of *bytes* |

A 0.9 threshold can result in 50%+ line reduction if the removed content was verbose examples, redundant explanations, or formatting. **Judge quality by semantic analysis, not size ratios.**

**Why 0.9 default**: Skill functionality is normally distributed across sections. Wide tails mean some "low importance" sections occasionally carry critical value for edge cases. At 0.9, you preserve more of the tail while still achieving meaningful compression.

### Mode 2: Token Target

Compress to exact token budget.

```bash
/skill-distiller path/to/skill.md --tokens=500
```

**Token estimation**: Uses 4 chars/token heuristic. Accuracy: +/-20% vs actual provider tokenization. For precise limits, verify with provider's tokenizer.

### Mode 3: One-Liner

Extreme compression for quick reference.

```bash
/skill-distiller path/to/skill.md --mode=oneliner
```

Produces 3-line summary: TRIGGER/ACTION/RESULT

---

## Protected Patterns

These patterns **must be preserved** even if they look verbose:

| Pattern | Why Protected |
|---------|---------------|
| YAML `name`/`description` | REQUIRED by Agent Skills spec |
| Task creation | Compaction resilience |
| N-count tracking | Observation workflow |
| Checkpoint/state | State recovery |
| BEFORE/AFTER | Self-calibration |

If a protected pattern is removed, the functionality score is penalized (-10% per pattern) and flagged explicitly in output.

---

## Advisory Patterns

These patterns improve efficiency but aren't required:

| Pattern | Impact if Removed |
|---------|-------------------|
| Parallel/serial decision | Suboptimal execution order |
| Performance hints | Slower but functional |
| Caching guidance | Works but inefficient |

Advisory patterns removed are **warned** but don't penalize the functionality score.

---

## Symbol Reference (MetaGlyph)

Native mathematical symbols LLMs understand from pre-training. Zero legend overhead.

| Symbol | Replaces | Example |
|--------|----------|---------|
| `→` | results in, leads to, produces | `trigger → action` |
| `⇒` | implies, therefore, thus | `condition ⇒ behavior` |
| `∈` | belongs to, is in, member of | `value ∈ {a, b, c}` |
| `∀` | for all, for every, for each | `∀ files: validate` |
| `¬` | not, doesn't, isn't | `¬empty → process` |
| `∃` | there exists, there is | `∃ config → load` |
| `∧` | and, also, plus | `valid ∧ safe → proceed` |
| `∨` | or, either | `error ∨ timeout → retry` |

**Application**: Symbols replace verbose phrases in compressed output. No legend needed in output—LLMs comprehend natively.

**Research**: Based on MetaGlyph (arXiv:2601.07354) - 62-81% compression with native symbols.

---

## Calibration

**Storage**: `.learnings/skill-distiller/calibration.jsonl`

Each compression run is logged with expected functionality score. User feedback updates the `actual` field, enabling calibration over time.

### Calibration Stages

| N-count | Output | Meaning |
|---------|--------|---------|
| N < 5 | `90% (uncalibrated - first 5 compressions build baseline)` | LLM-only estimate |
| N = 5-10 | `88% (building baseline, N=7)` | Gathering data |
| N > 10 | `88% +/- 4% (calibrated, N=12)` | Historical data informs CI |

### Feedback Recording

After using a compressed skill, report actual outcome to improve future estimates:

```bash
/skill-distiller feedback --id=c1 --actual=85 --outcome="worked"
```

**Outcome values**: `worked`, `partial`, `failed`

This updates the calibration entry, enabling the system to learn from real-world usage.

### Viewing Calibration Data

```bash
cat .learnings/skill-distiller/calibration.jsonl | jq -s 'length'  # Count entries
cat .learnings/skill-distiller/calibration.jsonl | jq -s 'map(select(.actual != null))' # Entries with feedback
```

---

## Self-Compression

This skill can compress itself (meta-recursive).

**Guardrails**:
- **Higher threshold**: Require 95% functionality (not 90%)
- **Recursion check**: Detect self-referential compression
- **Preserve original**: Output to SKILL.compressed.md, never overwrite
- **Manual verification**: Require human approval

**Why 0.95 threshold**: The distiller must remain fully functional to distill other skills. Capability loss compounds (0.95 x 0.95 = 0.90 at next level).

**Enforcement**: The 0.95 threshold is a documented guardrail, not an automated check. When compressing skill-distiller variants, manually verify you're using `--threshold=0.95` or higher. The formula variant (`SKILL.md`) should never be the input for self-compression.

---

## Error Handling

| Error | Recovery Hint |
|-------|---------------|
| No content | Provide a valid SKILL.md file path or pipe content via stdin |
| No frontmatter | Add `---` block with `name` and `description` |
| No trigger section | Add '## When to Use' for best results |
| Token target impossible | Use --mode=oneliner for extreme compression |
| LLM unavailable | Run 'ollama serve' for local, or set GEMINI_API_KEY |
| Already minimal | No compression possible at threshold Y |

---

## Future

Planned features not yet implemented:

| Flag | Description | Status |
|------|-------------|--------|
| `--with-ci` | Calculate confidence interval (3x LLM calls) | Planned |

---

## Related

| Variant | Tokens | Functionality |
|---------|--------|---------------|
| [skill-distiller](../) (main) | ~400 | ~90% (formula) |
| [compressed](../compressed/) | ~975 | ~90% (prose) |
| [oneliner](../oneliner/) | ~100 | ~70% |
| **reference** (this) | ~2,500 | ~90% |

*Token counts are estimates using 4 chars/token heuristic. Functionality scores are LLM-estimated.*

---

- [LLM Compression Research](../go-pbd/docs/research/2026-04-14-llm-compression-approaches.md) - MetaGlyph, LLMLingua, and 11 other techniques surveyed
- [skill-compression-support.md](../go-pbd/docs/plans/2026-04-14-skill-compression-support.md) - CLI-based compression (Option B)
- [Agent Skills Spec](https://agentskills.io/specification) - Required fields, size constraints
