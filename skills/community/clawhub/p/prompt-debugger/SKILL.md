---
name: prompt-debugger
description: Debug prompts that produce unexpected AI outputs — diagnose failure modes, identify ambiguity and conflicting instructions, test variations, compare model responses, and iteratively improve prompt quality.
---

# Prompt Debugger

When a prompt isn't working as expected, systematically diagnose why and fix it. Identifies common failure patterns (ambiguity, conflicting instructions, missing context, wrong format specification), tests variations, and produces an improved version.

Use when: "why isn't this prompt working", "debug my prompt", "improve this prompt", "the AI keeps doing X instead of Y", "prompt not producing expected output", "prompt optimization", or iterating on system prompts.

## Commands

### 1. `diagnose` — Analyze a Failing Prompt

Given a prompt and its undesired output, identify the root cause.

#### Step 1: Structural Analysis

Read the prompt and check for common failure patterns:

**Ambiguity Checks:**
- Vague instructions ("make it better", "be more specific", "improve this")
- Missing output format specification
- Unclear scope ("analyze this" — analyze what aspect?)
- Pronoun confusion ("it", "this", "that" without clear referent)
- Multiple possible interpretations of key terms

**Conflict Checks:**
- Contradictory instructions ("be concise" + "explain in detail")
- Competing priorities without ranking ("be accurate AND fast AND creative")
- Format conflicts (asking for both structured and freeform output)
- Tone conflicts ("be professional" + "be casual and fun")
- Length conflicts (word limits vs. comprehensive coverage)

**Context Checks:**
- Missing role/persona specification
- No examples of desired output
- Assumed knowledge not stated
- Missing constraints (length, format, audience, tone)
- No success criteria ("how would I know if the output is good?")

**Instruction Clarity:**
- Nested conditionals that are hard to follow
- Too many instructions competing for attention
- Critical instructions buried in the middle
- Instructions that depend on prior instructions but aren't ordered
- Implicit assumptions that should be explicit

#### Step 2: Failure Mode Classification

Categorize the issue:

| Failure Mode | Symptoms | Common Fix |
|-------------|----------|-----------|
| **Instruction Following** | Ignores specific requirements | Move to top, bold, repeat |
| **Format Violation** | Wrong output structure | Add explicit format example |
| **Hallucination** | Makes up facts | Add "only use provided info" |
| **Scope Creep** | Answers more than asked | Add "only address X, nothing else" |
| **Scope Deficit** | Answers less than asked | Break into numbered sub-questions |
| **Tone Mismatch** | Wrong voice/register | Provide tone examples |
| **Overthinking** | Too verbose/philosophical | Add "be direct, no preamble" |
| **Underthinking** | Too shallow/generic | Add "think step by step" + require specifics |
| **Context Window** | Loses early instructions | Repeat key constraints at end |

#### Step 3: Generate Fix Hypotheses

For each identified issue, propose specific prompt edits:

```
Issue 1: Ambiguous instruction "analyze the data"
  → Fix: "Analyze the data by calculating the mean, median, and standard deviation for each column. Report any outliers (>2 standard deviations from mean)."

Issue 2: Missing output format
  → Fix: Add "Output format: JSON with keys {summary, findings, recommendations}"

Issue 3: Conflicting constraints
  → Fix: "Prioritize accuracy over brevity. If you must choose between being complete and being concise, be complete."
```

### 2. `compare` — A/B Test Prompt Variations

Generate 3-5 variations of a prompt, each targeting a different failure mode fix.

```markdown
## Variation A: Original (baseline)
[original prompt]
Expected improvement: none (baseline for comparison)

## Variation B: Explicit format
[prompt + format specification]
Target fix: format violation

## Variation C: Role + examples
[prompt + persona + 2 examples]
Target fix: tone mismatch, underthinking

## Variation D: Constraints tightened
[prompt + explicit constraints + negative examples]
Target fix: scope creep, hallucination

## Variation E: Restructured
[reordered prompt with critical instructions first/last]
Target fix: instruction following
```

For each variation, explain what was changed and why.

### 3. `rewrite` — Produce an Improved Prompt

Apply all identified fixes to produce a single improved prompt.

**Rewrite principles:**
1. Critical instructions go first AND last (primacy + recency effects)
2. One instruction per line/bullet (no compound sentences)
3. Include 1-2 examples of desired output
4. Specify what NOT to do (negative examples) for common failure modes
5. Define success criteria explicitly
6. Use markdown formatting for structure (headers, bullets, bold for emphasis)
7. Add explicit output format specification

**Before/After format:**
```markdown
### Before
[original prompt — highlight problematic areas]

### After
[improved prompt — annotate what changed and why]

### Changes Made
1. Added role specification ("You are a senior data analyst...")
2. Replaced "analyze" with specific analytical steps
3. Added output format (JSON schema)
4. Moved length constraint to the end (recency)
5. Added negative example ("Do NOT include...")
```

### 4. `patterns` — Common Prompt Patterns Library

Reference of proven prompt patterns for common tasks:

**Chain of Thought:**
```
Think through this step by step:
1. First, identify...
2. Then, analyze...
3. Finally, recommend...
Show your reasoning for each step.
```

**Few-Shot:**
```
Here are examples of the expected output:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now process:
Input: [actual input]
Output:
```

**Constraint Sandwich:**
```
[CRITICAL CONSTRAINTS — read first]
[Main task instructions]
[CRITICAL CONSTRAINTS — repeated for emphasis]
```

**Persona + Task + Format:**
```
You are [specific role] with [specific expertise].
Your task is to [specific action] for [specific audience].
Output as [specific format] with [specific requirements].
```

**Self-Verification:**
```
After generating your response, verify:
- Does it address all N requirements?
- Is it under X words?
- Does it follow the specified format?
If not, revise before outputting.
```

### 5. `score` — Rate Prompt Quality

Score a prompt on multiple dimensions (0-10 each):

| Dimension | Score | Assessment |
|-----------|-------|-----------|
| Clarity | 7/10 | Instructions are clear but "analyze" is ambiguous |
| Specificity | 4/10 | Missing format, length, audience |
| Completeness | 6/10 | Has context but no examples |
| Consistency | 8/10 | No conflicting instructions |
| Testability | 3/10 | No success criteria defined |
| **Overall** | **5.6/10** | Needs format spec and examples |

Provide the top 3 improvements that would most increase the score.

### 6. `anti-patterns` — Detect Common Prompt Anti-Patterns

Scan a prompt for known problematic patterns:

- **Hedge language**: "Try to", "if possible", "maybe", "perhaps" (weakens instructions)
- **Overloading**: More than 7 distinct instructions (cognitive load)
- **Vague quantifiers**: "some", "several", "a few", "many" (replace with numbers)
- **Double negatives**: "don't not include" → "include"
- **Passive voice instructions**: "the data should be analyzed" → "analyze the data"
- **Escape hatches**: "unless you think otherwise" (invites non-compliance)
- **Meta-instructions**: Spending tokens on "you are an AI" preamble
- **Repeat-after-me**: Asking the AI to confirm instructions (wastes tokens)

## Output Formats

- **text** (default): Diagnostic report with annotated prompt
- **json**: `{diagnosis: {issues: [], failure_modes: [], fixes: []}, rewrite: "", score: {}, anti_patterns: []}`
- **markdown**: Report suitable for documentation or sharing

## Notes

- Works with any LLM prompt (system prompts, user prompts, agent instructions, SKILL.md files)
- Does not execute prompts — analyzes structure and content statically
- Failure mode classification is based on common patterns, not guaranteed causes
- For best results, provide both the prompt AND an example of the undesired output
- The rewrite is a starting point — always test with your specific model and use case
- Different models respond differently to the same prompt — fixes may need model-specific tuning
