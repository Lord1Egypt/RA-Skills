---
name: industrial-design-robot-brief
description: Use when the task is to find recent humanoid-robot papers and turn them into Chinese briefs for industrial designers, prioritizing design impact, user experience, and product-definition relevance over pure academic popularity.
---

# Industrial Design Robot Brief

Use this skill when the user wants humanoid-robot papers translated into Chinese and rewritten as briefs that industrial designers and product teams can quickly understand.

## Goal

Produce a daily brief from recent humanoid-robot papers.

Default behavior:
- collect papers from `yesterday` in the user's local timezone
- select the top `5` papers
- prioritize `industrial design`, `UX / trust`, and `product-definition` impact
- write in `Chinese`
- append the result to the same Feishu document
- place the newest day directly below the pinned header

## Workflow

1. Read [sources](./references/sources.md) to collect and rank candidates.
2. Use the design-impact scoring rules there to choose the final `5`.
3. Read [translator](./references/translator.md) before writing any paper brief.
4. Read [template](./references/template.md) and follow the exact section order.
5. Read [formatter](./references/formatter.md) before updating the Feishu document.
6. Run the checks in [quality-check](./references/quality-check.md) before finalizing.

## Output Standard

Every paper must help the reader answer:
- Why does this matter for the robot's external shape?
- Why does this matter for internal layout or packaging?
- Why does this matter for user trust, safety, or interaction?
- What kind of product or scenario does this suggest?

If a paper cannot clearly answer at least `2` of those `4` questions, it should usually not be in the final `5`.

## Defaults

- `date_range`: yesterday
- `count`: 5
- `language`: Chinese
- `audience`: industrial designers, UX designers, product teams
- `doc_name`: `🤖 Robot Paper Daily Brief`

## Hard Rules

- Do not fabricate arXiv IDs, DOI, author names, institutions, or metrics.
- Mark uncertainty explicitly with `待核实`, `未找到`, or `论文未公开该数据`.
- Separate `论文事实` from `设计判断` when making product or design inferences.
- Keep the daily update useful for someone with about `15 minutes` to read.
