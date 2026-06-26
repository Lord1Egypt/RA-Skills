# Prompt Expert — Examples (curated)

## 1. Refining a vague prompt

**Before:** `Help me write a better prompt for analyzing customer feedback.`  

**After:** Specify role, outputs (sentiment, themes, JSON keys), length constraints, and ask for review of `[ORIGINAL PROMPT HERE]`.

## 2. Custom instructions (agent YAML excerpt)

```yaml
---
name: data-analysis-agent
description: Financial data analysis and reporting
---
# Role + Do/Don't + output sections + scope (see full patterns in prior versions if needed)
```

Use: Do’s/Don’ts, fixed report sections, explicit scope and escalation.

## 3. Few-shot classification

Give category definitions + 2–3 labeled tickets + `Now classify: Ticket: "..." Category:`.

## 4. Chain-of-thought scaffold

`Step 1: problem → Step 2: factors → Step 3: options → Step 4: recommendation` + paste scenario.

## 5. XML-structured marketing prompt

`<metadata>`, `<instructions>`, `<constraints>`, `<format>`, optional `<examples>`.

## 6. Iterative refinement request

Paste current prompt, list failures, ask for: missed issues, fixes, revised prompt, changelog, test cases.

## 7. Anti-pattern vs improved

Replace “analyze and make it good” with metrics, format (e.g. table columns), and decision goal (e.g. Q4 revenue).

## 8. Prompt evaluation framework

Define happy path, ambiguous input, complex input, invalid input, regression case — expected output + pass criteria each.

## 9. Skill metadata template

```yaml
---
name: analyzing-financial-statements
description: One-line capability + primary use
---
# Overview, capabilities, use cases, limitations
```

## 10. Optimization checklist

Clarity · conciseness · completeness · testability · robustness (variation + errors + jailbreak resistance).
