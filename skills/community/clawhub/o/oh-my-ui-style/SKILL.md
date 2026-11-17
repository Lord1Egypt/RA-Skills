---
name: oh-my-ui-style
description: Ask whether the work is a whole admin platform or a single page, then render clickable, in-conversation proposals - shell structure first, palette second - so the user picks without leaving the chat, delegating design direction to an installed design skill when one fits; use when choosing visual direction before implementation, not when the project already has a design system or asked for the finished page.
---

# Oh My UI Style

Turn "make it look good" into a short sequence of clickable decisions inside the conversation, then hand the chosen tokens to implementation.

## Scope

Use for structure, style, palette, and layout-direction decisions on admin consoles, dashboards, internal tools, and single pages. Skip when the project already has a design system to follow, or when the user asked for the finished page - implement that directly.

## Step 0 - Ask the mode first

Ask one short question before generating anything:

- **整体管理平台** - login page, navigation shell, header, theme tokens, and the content area.
- **单个页面** - one page's own structure and styling inside an existing shell.

Rules:

- Skip the question when the request already states the mode ("整个后台", "这个列表页", "just this page").
- Ask at most one clarifying question. Infer modules from the project; when the user names them, use their names verbatim.
- Announce the mode in one line before rendering.

## Design source

Decide where the design direction comes from before writing any tokens.

1. Check the skills already loaded in this session for a design-direction skill: `frontend-design`, `ui-ux-pro-max`, `design-*`, `brand-*`, or any description covering visual design, design systems, or UI style.
2. If none is loaded, scan the frontmatter descriptions of `~/.codex/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md`, and `~/.config/magpie/library/skills/*/SKILL.md` for the same keywords.
3. When a fitting skill is found, read it and let it own palette, type roles, layout concept, and signature element. This skill then owns only three things: variants must differ structurally, the picker contract, and the selection handoff.
4. When a design skill exists but does not fit this product - another brand's guidelines, a different medium - say why it was skipped and continue.
5. When nothing fits, use the built-in fallback below.
6. Name the design source in the final reply ("direction from frontend-design" or "built-in fallback"). Never present freehand model choices as if they were a project standard.
7. If a known design skill such as `ui-ux-pro-max` is missing and would clearly improve the result, mention that skill-installer can add it.

## Built-in fallback

Use only when Design source found no fitting skill.

- Lock the brief in one pass: page name, the 3-4 core modules, framework or design-system constraints, light or dark or both. Infer defaults from the project where possible; ask at most one round of questions.
- Write the token plan first: 4-6 named hex values (surface, raised surface, border, text, primary, one semantic color), 2 type roles (display + body, plus a mono utility role for data-heavy screens), a one-sentence layout concept, and one signature element.
- Re-read the plan against the brief. If a proposal would fit any similar brief unchanged, revise that proposal before rendering.

## Variants

- Whole platform defaults to 5 shell proposals; a single page defaults to 4.
- Both counts are starting points, not limits. When the user asks for more, or the information architecture is deeper than the default set can express, extend to 6-8 and invent archetypes grounded in the project's real menu structure.
- Each variant must differ in layout and interaction, not just hue. Real archetypes to draw from: equal-weight quadrant grid, sequential pipeline, master-detail split, dense telemetry HUD.
- Name variants with descriptive words ("Bento 矩阵", "Pipeline 流水线"); never prefix them with numbers.
- Fill each mini interface with the project's real nouns - module names, field names, severity levels - not placeholder text.

## Mode A - Whole admin platform

Two steps, both rendered in the conversation.

Step 1, shell structure:

- Cover the shell explicitly: login, navigation, header/topbar, content area, theme tokens.
- Default seeds: icon rail, standard sidebar, top navigation, grouped sidebar, hybrid navigation. Treat this list as examples, not a closed set - add or replace shells to match the real menu depth.
- Every card shows: a short id, the name, a wireframe preview drawn in the dark ops example palette (real hex values, not grey placeholders), one line on which platform shape it fits, and the card's example tokens (surface / panel / primary / alert).
- Single select, with a persistent "current selection" bar and one confirm action.

Step 2, palette and type:

- Take the selected shell and render 3-4 palettes on that same shell. Do not change the structure.
- Each proposal shows the swatch strip, the type pairing, and the same shell preview in that palette.
- Single select again; then hand off the combined tokens.

## Mode B - Single page

- Default 4 proposals; more when asked.
- Keep the surrounding shell constant and vary the page itself: list + detail, table-first, card wall, split editor, dashboard.
- Each proposal includes its own dark palette preview, swatch strip, and type pairing.

## Rendering

Read the `visualize` skill and follow its fragment contract exactly before authoring.

- If the `visualize` skill is available, always render in the conversation. Never default to writing an HTML file the user must download or open separately.
- Write files only when the user explicitly asks for a file, or when no in-conversation surface exists; then fall back to imagegen mockups, and only then to `open_in_codex`.
- When a design skill's aesthetic rules conflict with the token guidance here, the design skill wins. The fragment contract, picker structure, and selection handoff always follow this skill and the `visualize` contract.
- Give the fragment root a unique id and scope every selector to it.
- Selection is single-select: clicking a card marks it selected, updates the bottom bar, and saves `window.openai.setWidgetState({ selectedScheme })`.
- The confirm button calls `window.openai.sendFollowUpMessage` with the full token string. Guard both host APIs.
- Bind `Tweak` where it adds something the picker does not already choose - for example the example accent inside the shell picker. Skip it when the control would duplicate the choice itself.
- Reflow to one column below 640px instead of shrinking the wireframes.
- Start from [assets/platform-shell-picker.html](assets/platform-shell-picker.html) for Mode A step 1 and [assets/style-picker-template.html](assets/style-picker-template.html) for step 2 or Mode B; replace placeholders instead of restructuring the shell.

## After the pick

- Restate the chosen tokens, write them as one CSS variable block in the project, and require later pages to consume only those variables.

## Quality bar

- Body text keeps at least 4.5:1 contrast on its own surface; state colors always pair with text or shape.
- Motion only where it encodes state, and honor `prefers-reduced-motion`.
- Keep one design source for all variants; never mix a design skill's direction with freehand fallback choices in the same set.
