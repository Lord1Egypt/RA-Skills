# Depth and Elevation Reference

## Table of Contents
1. The Layering Technique
2. Dual Shadow System
3. Inset Shadows
4. Gradient + Inner Shadow Combo
5. Semantic Z-Index Scale
6. Shadow Usage Guide
7. Dark Mode Shadow Adjustments
8. The "Remove Borders" Rule
9. Hover Elevation Pattern
10. Common Mistakes

---

## 1. The Layering Technique

The single highest-ROI technique for transforming flat UIs into ones that feel crafted. Three steps:

1. **Create color layers.** Generate 3-4 shades of your base color by incrementing lightness in OKLCH:
```css
--bg-deep:    oklch(0.18 0.01 var(--hue));   /* page background (deepest) */
--bg-base:    oklch(0.22 0.01 var(--hue));   /* card/section background */
--bg-raised:  oklch(0.26 0.012 var(--hue));  /* elevated interactive elements */
--bg-highest: oklch(0.30 0.015 var(--hue));  /* selected/active states */
```
In light mode, reverse the direction: the page is lightest, and elevated elements are slightly darker or lighter depending on the effect.

2. **Layer elements.** Darker backgrounds feel recessed. Lighter surfaces feel elevated. Stack your components accordingly: page → section → card → interactive element.

3. **Add dual shadows.** A light inset shadow on top combined with a dark shadow at the bottom creates realistic depth. See section 2 below.

---

## 2. Dual Shadow System

Combine a light inset highlight on the top edge with a dark drop shadow at the bottom. This simulates overhead light hitting a raised surface.

```css
/* Small: subtle, most use cases (cards at rest, navbar, buttons) */
--shadow-sm:
  inset 0 1px 0 0 oklch(1 0 0 / 0.05),
  0 1px 2px 0 oklch(0 0 0 / 0.15);

/* Medium: emphasis and hover states */
--shadow-md:
  inset 0 1px 0 0 oklch(1 0 0 / 0.08),
  0 2px 8px -2px oklch(0 0 0 / 0.2);

/* Large: modals, popovers, focused cards */
--shadow-lg:
  inset 0 1px 0 0 oklch(1 0 0 / 0.1),
  0 8px 24px -4px oklch(0 0 0 / 0.25);

/* Extra large: hero overlays, dramatic emphasis */
--shadow-xl:
  0 16px 48px -8px oklch(0 0 0 / 0.3),
  0 4px 12px -2px oklch(0 0 0 / 0.15);
```

These values use OKLCH alpha for consistency with your color tokens. Adapt the hue to match your palette if desired (e.g., `oklch(0 0 0 / 0.15)` could become `oklch(0 0.01 var(--hue) / 0.15)` for tinted shadows).

---

## 3. Inset Shadows

For elements that should feel *recessed* into the surface (input fields, progress bars, table cells, code blocks):

```css
.recessed {
  box-shadow:
    inset 0 2px 4px 0 oklch(0 0 0 / 0.15),   /* dark shadow at top */
    inset 0 -1px 0 0 oklch(1 0 0 / 0.05);     /* subtle light at bottom */
}
```

Inset shadows reverse the mental model: instead of floating above the surface, the element sits below it. Use this for:
- Text inputs (the field feels carved into the form)
- Progress bar tracks (the bar sits inside a groove)
- Recessed stat cards (metrics feel embedded, not floating)

---

## 4. Gradient + Inner Shadow Combo

Simulates directional light hitting a raised surface from above. Powerful for selected cards, active states, and CTAs:

```css
.elevated-card {
  background: linear-gradient(
    to bottom,
    oklch(0.28 0.015 var(--hue)),  /* lighter at top (light source) */
    oklch(0.24 0.01 var(--hue))    /* darker at bottom */
  );
  box-shadow:
    inset 0 1px 0 0 oklch(1 0 0 / 0.08),  /* highlight at top edge */
    0 2px 8px -2px oklch(0 0 0 / 0.2);     /* shadow beneath */
}
```

This combination makes elements feel physically present. Reserve it for the most important interactive elements on the page -- overuse dilutes the effect.

---

## 5. Semantic Z-Index Scale

Use named z-index values instead of magic numbers. This prevents z-index wars and makes the stacking context explicit:

```css
--z-dropdown: 100;
--z-sticky:   200;
--z-fixed:    300;
--z-modal:    400;
--z-toast:    500;
--z-tooltip:  600;
```

Rules:
- Never use bare numbers. Always reference the variable.
- Never go above 600 unless you have a documented reason.
- Modals need a backdrop at `--z-modal - 1` (399).
- Toasts should float above modals so errors are visible during dialogs.

---

## 6. Shadow Usage Guide

| Element | Shadow Level | Additional Treatment |
|---------|-------------|---------------------|
| Cards (default) | sm | -- |
| Cards (hover) | md | transition 150ms |
| Selected card | md + gradient | light inset top |
| Modal / dialog | xl | overlay backdrop |
| Dropdown menu | lg | -- |
| Navbar (sticky) | sm | only when scrolled |
| Input (focus) | -- | accent ring instead |
| Recessed element | inset | dark top + light bottom |
| Progress bar | inset sm | inside container |
| Buttons (default) | sm | -- |
| Buttons (active) | inset sm | press-in effect |
| Tooltip | md | -- |

Not every element needs a shadow. Use shadows to communicate interactive hierarchy: elements the user can act on float above static content.

---

## 7. Dark Mode Shadow Adjustments

Shadows are far less visible against dark backgrounds. Compensate with these techniques:

1. **Increase shadow opacity** by 0.05-0.10 compared to light mode values
2. **Add a subtle border** (1px `oklch(1 0 0 / 0.05)`) for edge definition where shadows alone are too faint
3. **Use inner glow** instead of drop shadows for the "elevated" feeling on small elements
4. **Higher surface = lighter background** -- in dark mode this is the primary depth cue, more important than shadows

```css
[data-theme="dark"] {
  --shadow-sm:
    inset 0 1px 0 0 oklch(1 0 0 / 0.03),
    0 1px 3px 0 oklch(0 0 0 / 0.25);
  --shadow-md:
    inset 0 1px 0 0 oklch(1 0 0 / 0.05),
    0 3px 12px -3px oklch(0 0 0 / 0.35);
}
```

---

## 8. The "Remove Borders" Rule

When you have established a clear color layering system (darker background → lighter card → lightest interactive element), borders on the lighter elements become redundant. The color contrast already creates visual separation. Remove them.

Keep borders only where:
- Color layering alone does not provide enough contrast (e.g., two surfaces with very similar lightness)
- You need to indicate a semantic boundary (form fields, table cells)
- The element is interactive and the border communicates state (focus, error)

This rule significantly reduces visual noise and makes the layering technique more effective.

---

## 9. Hover Elevation Pattern

```css
.card {
  box-shadow: var(--shadow-sm);
  transition: box-shadow 150ms ease-out, transform 150ms ease-out;
}
.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
```

Key constraints:
- Keep the translateY subtle: 1-3px maximum. Exaggerated lifts (5px+) feel cheap and dated.
- Always transition both shadow and transform together for a cohesive effect.
- On touch devices, this hover state should not apply (use `@media (hover: hover)`).

---

## 10. Common Mistakes

- Using the same `box-shadow` on every element (no hierarchy, everything looks the same)
- Shadow blur radius too large (20px+ on cards creates a fuzzy, unfocused look)
- Forgetting to adjust shadows for dark mode (invisible shadows destroy the depth system)
- Overusing shadows on flat, decorative elements that do not need elevation
- Using `filter: drop-shadow()` when `box-shadow` would suffice (drop-shadow does not support inset and renders differently)
- Relying solely on shadows for depth without the color layering foundation (shadows alone look stuck-on)
- Hard-coded z-index values like `z-index: 9999` (always use the semantic scale)
