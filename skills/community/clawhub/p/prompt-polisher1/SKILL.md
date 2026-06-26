---
name: prompt-polisher
description: Rewrite rough goals, scattered notes, or vague requests into clear, actionable prompts with explicit objective, constraints, output format, and missing assumptions. Use when Codex needs to turn a messy idea into a better prompt for writing, coding, planning, research, content generation, or general task delegation.
---

# Prompt Polisher

## Overview

Turn an incomplete request into a prompt that is easier for another agent or model to execute well.
Keep the user's intent intact while removing ambiguity, adding structure, and stating assumptions clearly.

## Workflow

1. Identify the core goal in the user's rough request.
2. Extract any concrete constraints that are already present: audience, tone, format, length, platform, deadline, tools, or exclusions.
3. Detect what is missing but necessary for reliable execution.
4. Fill only low-risk gaps with brief assumptions. Label assumptions explicitly instead of presenting them as facts.
5. Rewrite the request into a compact prompt with clear sections.
6. If the request is still under-specified, provide a best-effort prompt plus a short list of the most important follow-up questions.

## Output Shape

Prefer this structure when rewriting:

- Goal
- Context
- Constraints
- Desired Output
- Assumptions
- Final Prompt

Omit empty sections. Keep the final prompt concise and ready to paste.

## Prompting Rules

- Preserve the original intent; do not silently change the task.
- Prefer concrete verbs over generic wording.
- Convert fuzzy asks like "make it better" into measurable instructions.
- Add output formatting when it helps execution, such as bullet list, table, JSON, checklist, or step-by-step plan.
- Avoid over-engineering simple requests. A short request should become a short polished prompt.
- When the user already gave enough detail, lightly polish instead of expanding aggressively.

## Common Transformations

- Replace vague verbs with precise actions.
- Separate background information from required deliverables.
- Turn implied preferences into explicit constraints.
- State the expected audience or reader when relevant.
- Add success criteria when quality is otherwise subjective.

## Example

Rough request:

> Write a product post for Xiaohongshu. Make it sound young and natural, not fake.

Polished prompt:

> Write a Xiaohongshu product post for readers aged 20 to 30. Use a natural, young, and sincere tone without exaggerated marketing language. First provide 3 title options, then provide 1 main post. Keep the main post under 300 Chinese characters. Highlight real usage scenarios, core selling points, and user benefits. Avoid absolute claims. Output in Chinese.

If critical details are missing, append up to 3 short follow-up questions after the prompt.
