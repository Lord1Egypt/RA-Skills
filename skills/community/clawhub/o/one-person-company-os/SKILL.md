---
name: one-person-company-os
description: Build a visual operating cockpit for an AI-native one-person company across promise, buyer, product, delivery, cash, learning, and assets. / 为 AI 一人公司建立可视化经营驾驶舱，覆盖价值承诺、买家、产品、交付、回款、学习与资产。
---

# One Person Company OS v1.0

Treat the user as the founder and final decision-maker.
This skill builds and advances a visual operating cockpit for a one-person company.

中文说明：把用户视为创始人与最终决策者。本技能用于建立并推进一人公司的可视化经营驾驶舱。

## Default Language Policy

- Chinese in -> Chinese runtime and materials by default.
- English in -> English runtime and materials by default.
- Localize the full user-visible workspace surface to the founder language.
- Keep only the hidden machine-state path stable at `.opcos/state/current-state.json`.
- Do not output bilingual deliverables unless the user explicitly asks for bilingual output.

## v1.0 Product Contract

The visible operating model is:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

Every serious run should keep the founder oriented around the current goal, bottleneck, primary arena, shortest action, and saved workspace outputs.

- The first downloaded HTML page is the operating cockpit.
- Deterministic SVG visuals carry exact operating data.
- AI images are optional creative assets for covers and launch posts, not required runtime output.

## Runtime Requirements And Safety Boundary

- Script mode expects an existing local `Python 3.7+`.
- `scripts/ensure_python_runtime.py` inspects compatibility and prints manual install guidance only.
- The marketplace build must not auto-install system packages.
- Persist changes only inside the founder-approved workspace.
- Do not request unrelated credentials or secrets.
- Do not require image generation or API keys for normal operation.

## Primary Entry Intents

Use this skill when the user wants to:

- start a one-person company from an AI product idea
- define a sellable promise and first buyer
- see the current bottleneck in a visual operating cockpit
- advance product, sales, delivery, cash, learning, or assets
- generate a download-friendly workspace with HTML, markdown, DOCX, and visual assets
- create optional AI-image prompts for launch or promotion

## Workspace Output

Chinese founders get:

- `阅读版/00-经营驾驶舱.html`
- `视觉素材/business-loop.svg`
- `视觉素材/revenue-pipeline.svg`
- `视觉素材/ai-image-prompts.md`

English founders get:

- `reading/00-operating-cockpit.html`
- `visual-kit/business-loop.svg`
- `visual-kit/revenue-pipeline.svg`
- `visual-kit/ai-image-prompts.md`

Markdown remains the editable source.
Numbered DOCX files under `产物/` or `artifacts/` remain the formal deliverables.

## Runtime Contract

Every serious run should clarify:

- the primary goal
- the current bottleneck
- the primary arena: `sales / product / delivery / cash / asset`
- the shortest action today
- what changed inside the approved workspace
- what to open next in the operating cockpit

## Non-Negotiable Rules

- Do not output document specifications instead of final documents.
- Do not add status words to completed file names.
- Do not pretend content is saved when it is still only in chat.
- Do not treat product development, sales, delivery, and cash as unrelated systems.
- Do not replace the operating cockpit with internal workflow mechanics.
- Keep the founder as the approval boundary for launch claims, pricing, budget, legal, or other high-risk actions.
- Do not auto-install system packages from this skill.
- Do not write outside the approved workspace.

## Recommended Commands

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/init_business.py "北辰实验室" --path ./workspace --product-name "北辰助手" --target-user "独立开发者" --core-problem "还没有一个真正能持续推进产品和成交的一人公司系统" --product-pitch "一个帮助独立开发者把产品做出来并卖出去的一人公司控制系统" --confirmed
python3 scripts/validate_release.py
```
