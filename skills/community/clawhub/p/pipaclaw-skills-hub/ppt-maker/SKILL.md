---
name: ppt-maker
description: "Single front-door skill for presentation work. Use when a user wants to make a PPT, keynote, proposal deck, investor deck, sales deck, training deck, or presentation from documents, notes, images, or data. This skill should internally orchestrate intake, story, evidence, structure, design, review, and export workers while keeping the current stage visible to the user."
---

# PPT Maker

This is the only public entrypoint for PPT work.

Use it when the user says broad things like:
- "帮我做一个 PPT"
- "我要做提案 / 路演 / 培训 deck"
- "我有一堆材料，帮我整理成演示"
- "先不知道怎么做这份 PPT"

The user should not need to choose sub-skills. Internally, this skill should behave like a small PPT team with worker handoffs and visible stage reporting.

PPT is a decision interface, not decoration. Read `references/first-principles-and-quality-bar.md` before changing the workflow or quality gates.

## Control Room Contract

Always expose a short status block when the work is non-trivial:

- `Stage`
- `Current Owner`
- `Current Gate`
- `Current Artifact`
- `Active Workers`
- `Blocker`
- `Next Action`

Use the role names from `references/control-room.md`.

Use stage names from `references/worker-playbooks.md`:
- `intake`
- `story`
- `evidence`
- `outline`
- `design`
- `draft`
- `review`
- `export`

If the user has only given a vague topic, stay in `intake`. Do not jump to slides.

## Intake

Do not behave like a survey form.

Ask only the minimum questions that materially change the deck:
- what decision this deck must drive
- who the audience is
- what the usage scene is: meeting, roadshow, async send, keynote, bid, training
- what source materials already exist
- where the file will actually be opened and edited: desktop office, WeChat, or both

Do not ask the user to choose design-internal variables unless there is a real brand or delivery conflict:
- page layout family
- card density
- palette nuances
- typography pairing
- visual rhythm or section pacing

Those are internal team decisions. The user should only be pulled in when the choice would materially change meaning, brand compliance, or delivery compatibility.

Before leaving intake, also capture the highest-impact polish constraints when relevant:
- preferred style or template reference, including template-library preference such as iSlide
- header / footer / page-number policy
- citation policy for evidence-heavy decks
- must-include sections and must-avoid elements
- delivery target and editing surface: `desktop-editable`, `wechat-editable-safe`, or `both`

If materials are fragmented, ask for one zip bundle. Read `references/material-bundle.md`.
Read `references/input-boundary-contract.md` before changing intake rules.
Read `references/delivery-compatibility.md` before locking export assumptions.

If the user refuses more questions, make the smallest explicit assumptions and continue. Do not hide the assumptions.
Default to making reasonable deck-design assumptions rather than turning design work into a questionnaire.

## Internal Workers

This skill internally orchestrates these workers:

- `Producer`
Owns intake, brief completion, and assumption logging.

- `Story Strategist`
Owns narrative pattern, opening tension, core argument, and closing ask.

- `Research Analyst`
Owns fact extraction, material cleanup, proof-gap analysis, and asset mapping.

- `Slide Architect`
Owns one-job-per-slide sequencing and page-level evidence allocation.

- `Design Director`
Owns visual direction, layout family, media policy, and template adaptation.

- `Deck Designer`
Owns slide-by-slide copy, asset placement, and speaker-note-ready deck specs.

- `Review Editor`
Owns acceptance review and rejection of weak drafts.

- `Export Operator`
Owns `.pptx` generation and local artifact delivery.

Read `references/worker-playbooks.md` to decide who should own the current stage.

## Worker Orchestration

Operate like a producer directing a team, not like one blob generating slides.

Default sequencing:
1. `Producer` clears intake.
2. `Story Strategist` chooses the argument.
3. `Research Analyst` validates proof and materials.
4. `Slide Architect` creates the page sequence.
5. `Design Director` sets visual policy.
6. `Deck Designer` writes the full deck pack.
7. `Review Editor` blocks weak output.
8. `Export Operator` generates final files.

Parallelism rule:
- After intake passes, `Story Strategist` and `Research Analyst` may work in parallel if the brief is stable.
- After the outline exists, `Design Director` may start while `Research Analyst` finishes low-risk asset cleanup.
- `Export Operator` must never start before `Review Editor` passes the deck.

When reporting progress to the user, speak in terms of stage ownership:
- what stage the deck is in now
- which worker owns the blocker
- what artifact was just completed
- what will happen next

Do not expose internal worker uncertainty as user homework. If the team is debating layout, page rhythm, or style variants inside a stable brief, resolve it internally.

Read `references/team-gates.md` before changing stage ownership, readiness rules, or rework routing.

## Template Intelligence

Do not design from scratch when the deck clearly belongs to a familiar business scene.

The `Design Director` should:
- read `references/template-family-recipes.md`
- read `references/template-library-architecture.md`
- read `references/typography-and-font-safety.md`
- identify the closest template family
- explain why that family fits the scene
- then choose a palette recipe from `references/color-system-playbook.md`

Use template families as reference grammar, not as assets to copy directly.

At minimum, the design stage should resolve:
- `style`
- `template family`
- `palette recipe`
- `theme key`
- `delivery compatibility profile`

If the user provides a reference PPT, template screenshot, or template-library preference such as iSlide, infer the family from that material before laying out pages.

If the user will open or forward the deck inside WeChat, the `Design Director` must explicitly switch into a WeChat-safe editable profile:
- keep text editable
- keep tables editable
- keep simple charts editable
- avoid fragile default font choices
- rasterize only decorative layers when needed
- avoid layouts that become visually blank if text rendering degrades

## Public Package Boundary

This public skill package should only contain:
- the user-facing workflow contract in `SKILL.md`
- agent metadata under `agents/`
- reusable operating references under `references/`

Do not put implementation-specific code in this package:
- no backend services
- no local runtime or exporter code
- no test harnesses
- no sample customer materials or private template assets
- no build output or dependencies

## Expected Outputs

Even though implementation lives elsewhere, the workflow should still behave like a visible PPT team and produce stage artifacts such as:
- intake summary
- story pack
- evidence audit
- page jobs
- visual direction
- review verdict
- final delivery plan

For final delivery, the workflow should prefer:
- native `.pptx` as the user-facing attachment
- browser preview as a separate preview link when available
- explicit status reporting for the current stage, owner, gate, and next action

The default user-facing path should not show a low-value rough draft.
Prefer this reveal sequence:
- reviewed intake summary when core facts are still unclear
- reviewed outline when the story or fact basis needs confirmation
- reviewed near-final deck when the team can already stand behind the page logic and visuals

If the user needs editing and WeChat is part of the actual delivery path, the workflow should default to two editable exports:
- `full-fidelity.pptx`
- `wechat-safe-editable.pptx`

The WeChat-safe file is not a PDF fallback. It must remain editable.

## Guardrails

- Do not act like a one-shot slide generator when intake is incomplete.
- Do not force the user to choose internal worker names.
- Do not keep status vague. Always name the current stage and the current owner.
- Do not let downstream stages hide upstream gaps. Missing audience is a Producer problem, weak proof is a Research problem, overloaded slides are a Slide Architect problem.
- Do not turn layout, palette, or typography into unnecessary user decisions.
- Do not surface shallow "first draft" output unless the user explicitly asked for a rough draft.
- Do not use an image model as a shortcut for real charts, tables, or editable diagrams.
- Do not invent business-critical facts without labeling them as assumptions and routing them through a fact lock.
- If the user asks for a final file, only export after the review gate passes.
- Do not assume a desktop-safe `.pptx` is automatically WeChat-safe.
- Do not ship a WeChat-targeted deck with fragile default fonts or text-only pages that would appear blank if the local viewer drops text rendering.

## References

- Read `references/control-room.md` for role ownership, handoffs, and artifact names.
- Read `references/worker-playbooks.md` for worker-specific operating rules and stage ownership.
- Read `references/first-principles-and-quality-bar.md` for the product definition of a good PPT.
- Read `references/input-boundary-contract.md` for the line between user-provided facts, system inference, and AI generation.
- Read `references/confirmation-policy.md` before changing when the user must confirm versus when the team can auto-continue.
- Read `references/team-gates.md` for the stage contract and rework routing.
- Read `references/material-bundle.md` when materials are missing, fragmented, or need a zip bundle.
- Read `references/deck-patterns.md` to choose the right narrative arc and default slide sequence.
- Read `references/style-presets.md` to choose the right visual system and layout family.
- Read `references/template-family-recipes.md` to map the deck into a recognizable template family instead of improvising every page.
- Read `references/template-library-architecture.md` to keep provider, family, page-recipe, and rendering responsibilities separated.
- Read `references/color-system-playbook.md` to choose a palette recipe and chart color policy.
- Read `references/typography-and-font-safety.md` before locking Chinese/English font policy or WeChat-safe text rendering assumptions.
- Read `references/slide-quality-checklist.md` before finalizing a deck or revising one.
- Read `references/delivery-compatibility.md` before promising export behavior for desktop, WeChat, or mixed delivery paths.
