---
title: Final Design Review Checklist
impact: HIGH
impactDescription: Designs submitted without final review are likely to include issues such as missing tokens, accessibility failures, and AI-pattern artifacts.
tags: showcase,checklist,review,quality,validate
---

## Final Design Review Checklist

After completing the design, you must pass the checklist below. If any item fails, fix it before submission.

### 🎨 Tokens & Colors

- [ ] Do all `fill`, `fontSize`, `padding`, and `gap` values reference tokens (`$`)?
- [ ] Are there no hardcoded hex colors (`#XXXXXX`) or raw px numbers?
- [ ] Are both light/dark theme tokens fully defined?
- [ ] Does it meet WCAG AA contrast (4.5:1 or higher)?
- [ ] Does it follow the 60-30-10 color ratio?

### 📐 Layout & Spacing

- [ ] Does every container frame include a `layout` property? (`"none"` prohibited except for overlay/badge/modal containers per z-order rule)
- [ ] Are there no empty frame spacers?
- [ ] Are all gap/padding values multiples of 4?
- [ ] Is `textGrowth` specified on text nodes?
- [ ] Are overlays/badges at the end of the children array?

### ✍️ Typography

- [ ] Are you using a Display+Body pairing instead of Inter alone?
- [ ] Is at least a 6-step type scale used?
- [ ] Are weights by role (400/500/600/700) differentiated?
- [ ] Is body text column width capped at 640–680px?
- [ ] Is lineHeight applied differently by size?

### 🧩 Components

- [ ] Did you search existing reusable items and reuse via ref?
- [ ] Do component names use `category/variant` slash format?
- [ ] Is a slot declared for the content area?
- [ ] Are newly created components independent reusable items per variant?

### 🚫 Anti-AI Aesthetic

- [ ] Are there no AI-typical colors (Tailwind blue-500, purple→blue gradients)?
- [ ] Is it not the typical hero→3 cards→CTA→footer layout?
- [ ] No Lorem ipsum / repeated "Get Started" × 3 / "10K+ Users" clichés?
- [ ] No decorative blobs or excessive shadows?

### 📱 Responsive

- [ ] Are there three breakpoint frames (375/768/1440)?
- [ ] Does each frame share the same reusable components via ref?

### ✅ Final Check

- [ ] Confirm no errors with `node scripts/validate-pen.mjs`
- [ ] Are all ids unique?
- [ ] Does the showcase frame include color/type/component inventory?
