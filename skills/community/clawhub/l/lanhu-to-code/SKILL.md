---
name: lanhu-to-code
description: Convert Lanhu (蓝湖) design drafts, specs, screenshots, exported assets, annotations, or design links into frontend code. Use when Codex is asked to implement UI from Lanhu, restore a design to HTML/CSS/React/Vue/Tailwind, match a 蓝湖设计稿, inspect design measurements, generate components from Lanhu specs, or visually verify code against a Lanhu mockup.
---

# Lanhu To Code

## Overview

Use this skill to turn Lanhu design material into production-ready frontend code while preserving the current project's conventions. Treat the design as the source of truth, but make explicit assumptions when Lanhu data is incomplete or inaccessible.

## Workflow

1. Collect design inputs.
   - Ask for the Lanhu link, screenshots, exported images, annotations, CSS snippets, dimensions, and asset package if they are not already provided.
   - If the Lanhu link requires login or is inaccessible, work from screenshots and any exported specs the user can provide.
   - For visual tasks, use browser or image inspection tools when available rather than relying only on text descriptions.

2. Inspect the target codebase.
   - Identify framework, styling system, component library, asset conventions, routing, and existing UI patterns.
   - Reuse existing components and tokens before introducing new primitives.
   - Do not create a landing page or explanatory wrapper unless the design explicitly calls for it.

3. Extract the design system facts.
   - Capture canvas size, layout grid, spacing, typography, colors, radii, borders, shadows, imagery, icons, states, and responsive behavior.
   - Prefer exact values from Lanhu specs. When only screenshots exist, estimate carefully and record assumptions.
   - Read `references/visual-checklist.md` when implementing a full page, dense component, or anything requiring close visual fidelity.

4. Implement the UI.
   - Build the actual requested screen or component, not a placeholder.
   - Map repeated elements into reusable components only when repetition or local project patterns justify it.
   - Use semantic HTML and accessible controls. Preserve keyboard and focus behavior for interactive elements.
   - Import or copy provided assets into the project's established asset location. Do not hotlink private Lanhu assets.

5. Match visual fidelity.
   - Start a local dev server when the project requires one.
   - Capture screenshots at the design's native viewport and at relevant responsive breakpoints.
   - Compare layout, spacing, typography, colors, image cropping, and interaction states against the Lanhu material.
   - Iterate until obvious mismatches are fixed or explicitly called out as blocked by missing design data.

6. Deliver with evidence.
   - List changed files, verification commands, and screenshot/browser checks performed.
   - Mention any assumptions, missing assets, inaccessible Lanhu data, or intentional deviations from the design.

## Implementation Guidance

- Favor CSS variables, design tokens, theme utilities, and existing component props over one-off values when the project already has them.
- Use absolute pixel values where the design is fixed-format, and responsive constraints where the UI must adapt.
- Keep text from overflowing controls or overlapping neighboring content.
- Use icon libraries already present in the project. If no icon library exists, use provided exported icons or simple inline SVG only for small, necessary symbols.
- Preserve image aspect ratios and object positioning from the design. Use real provided images when available.
- Avoid decorative embellishments not present in the Lanhu design.

## Missing Or Ambiguous Data

If design data is incomplete, proceed with best judgment after checking available artifacts. Call out assumptions at the end instead of blocking unless a core requirement cannot be inferred, such as the target framework, the only available screen, or access to required assets.

## User Request Examples

- "用蓝湖设计稿还原这个页面"
- "把这个 Lanhu 链接做成 React 组件"
- "根据蓝湖标注实现移动端页面"
- "按这个蓝湖截图写 Tailwind 页面，并帮我对齐视觉"
- "把蓝湖导出的素材接到现有 Vue 项目里"
