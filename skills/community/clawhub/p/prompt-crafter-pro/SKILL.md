---
name: "prompt-crafter-pro"
description: "6-dimension AI prompt diagnosis, rewrite, and test-case generation. Analyze, score, and optimize prompts for any LLM (GPT-4o, Claude, DeepSeek)."
---

# Prompt Crafter Pro

Systematically diagnose and optimize AI prompts. Prompt Crafter Pro analyzes your prompts across **6 dimensions**, scores them, and generates optimized versions with test cases — so your AI output is precise, consistent, and reliable.

## Why Prompt Crafter Pro?

- **Stop guessing**: Get a clear diagnostic score for each dimension of your prompt.
- **Optimize for any model**: Adapt prompts for GPT-4o, Claude, DeepSeek, or any LLM.
- **Test before you ship**: Get 3-5 test inputs to validate your optimized prompt.
- **Learn as you go**: Each optimization explains *why* the change matters, improving your prompt engineering skills.

## The 6 Dimensions

| # | Dimension | What It Measures | Max Score |
|---|-----------|-----------------|-----------|
| 1 | 👤 Role | Is the AI given a clear persona/expert identity? | 5 |
| 2 | 🎯 Task | Is the core instruction specific and unambiguous? | 5 |
| 3 | 📖 Context | Does the prompt provide sufficient background? | 5 |
| 4 | 🚧 Constraints | Are boundaries, exclusions, and limits defined? | 5 |
| 5 | 📋 Output Format | Is the expected output structure clearly specified? | 5 |
| 6 | 🧪 Examples | Does the prompt include few-shot examples? | 5 |
| | **Total** | | **30** |

## Workflow (8 Steps)

```
Input: Current prompt text + goal description (what + expected output + current issues)
↓
[1] Parse prompt into 6 dimensions — identify what's present and what's missing
[2] Score each dimension 0-5 — diagnose weak spots
[3] Generate dimension gap report — explain what's missing and why it matters
[4] Two rewrite options:
    → V1 Enhanced: Strengthen existing structure without changing intent
    → V2 Full Rewrite: Complete restructure with all 6 dimensions filled
[5] Auto-complete: Fill role, output format, constraints, and rejection examples
[6] Generate 3-5 test cases — pre-built inputs to validate the optimized prompt
[7] Model-specific adaptation (optional): GPT-4o / Claude / DeepSeek
[8] Output: Side-by-side comparison + dimension scores + test cases
↓
Output: Optimized prompt + dimension scoring + modification notes + test cases
```

## Sample Prompts

### Sample 1: Vague extraction prompt
> "I use 'Extract key info from this document.' but the output format changes every time. Help me fix it."

### Sample 2: Role-less sales prompt
> "My sales email generator prompt works but the tone varies wildly. Make it consistent."

### Sample 3: Model migration
> "I have a prompt that works well with Claude but I need it optimized for DeepSeek. The output structure changes."

### Sample 4: Full rewrite needed
> "Write a prompt that turns meeting transcripts into action items. It needs to handle 30-min to 2-hour meetings."

### Sample 5: Constraint injection
> "My code generator prompt produces 300-line functions when I want 20-line utilities. Help me add constraints."

## First-Success Path

```
1. Describe your current prompt and what you want it to do
2. The skill will score your prompt across 6 dimensions (0-5 each, max 30)
3. Review the dimension gap report to understand weak spots
4. Choose V1 Enhanced (light touch) or V2 Full Rewrite (complete restructure)
5. Use the generated test cases to validate the optimized prompt
6. Optionally request model-specific adaptation
```

## Dimension Diagnostic Example

### Input Prompt
> "From this contract, extract key information and output it to me."

### 6-Dimension Score
| Dimension | Score | Why |
|-----------|-------|-----|
| 👤 Role | 0 | No persona defined |
| 🎯 Task | 1 | "Key information" is vague — not specific |
| 📖 Context | 0 | No background, document type, or scope |
| 🚧 Constraints | 0 | No boundaries, exclusions, or guardrails |
| 📋 Output Format | 0 | No structure defined |
| 🧪 Examples | 0 | No few-shot examples |
| **Total** | **1/30** | **Severely under-specified** |

### Optimized V2 (Full Rewrite)

```markdown
You are an expert contract analyst with 15 years of experience in Chinese business law.

TASK: Extract and structure the following 8 categories from the attached contract:
1. Parties involved (full legal names, roles)
2. Effective date and term
3. Payment terms (amount, schedule, currency)
4. Termination clauses (notice period, conditions, penalties)
5. Liability and indemnification (caps, exclusions)
6. Confidentiality obligations (duration, scope)
7. Dispute resolution (jurisdiction, arbitration)
8. Special conditions or unusual clauses

CONTEXT: This is a service agreement between a Chinese tech company and a foreign vendor. The contract is governed by PRC law.

CONSTRAINTS:
- Only extract facts — do not interpret or evaluate
- If a category is absent from the contract, mark it as "Not specified"
- Do not redact, summarize, or omit any numerical values
- Maximum output length: 2 pages

OUTPUT FORMAT:
```json
{
  "contract_type": "...",
  "parties": [{"name": "...", "role": "..."}],
  "effective_date": "...",
  "term": "...",
  "payment_terms": {...},
  "termination": {...},
  "liability": {...},
  "confidentiality": {...},
  "dispute_resolution": {...},
  "special_conditions": [...]
}
```

EXAMPLE:
Input: (short contract snippet)
Output: { "parties": [{"name": "Beijing Tech Co., Ltd.", "role": "Service Provider"}] }
```

## Model-Specific Adaptation Guide

| Model | Strength | Adaptation Tip |
|-------|----------|----------------|
| GPT-4o | Balances instruction-following and creativity | Add explicit output format, examples helpful |
| Claude | Excellent at structured output, follows XML | Use XML tags in prompts, split role/task/context |
| DeepSeek | Strong at reasoning with multi-step instructions | Provide step-by-step chain-of-thought, clear separation |
| Gemini | Good with long context, multi-modal | Keep instructions front-loaded, examples at end |

## Tags

`prompt-crafter-pro`, `prompt-engineering`, `llm`, `optimization`, `prompt`, `gpt`, `claude`, `deepseek`, `ai-productivity`
