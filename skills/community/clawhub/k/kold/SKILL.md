---
name: kold-frontend-design
description: "Use when building, implementing, or refactoring frontend UI — components, pages, layouts, interactions, or any visual work in pure HTML/CSS/JS. Use when integrating design tokens, writing CSS custom properties, implementing dark mode, fixing responsiveness, or optimizing accessibility. Use when aesthetic judgment is needed — typography, color harmony, spacing rhythm, visual hierarchy. Trigger phrases: '帮我写一个卡片组件'、'实现这个设计'、'布局在手机上乱了'、'帮我做 dark mode'、'检查一下无障碍'、'这个间距看起来不对'、'帮我设计一个登录页面'、'CSS 怎么写更优雅'"
version: 0.1.0
---

# Kold Frontend Design Skill

When this skill is active, every visual artifact you produce must be precise, token-driven, accessible, and aesthetically sound. Pure HTML/CSS/JS only.

## Core Principles

1. **Design tokens first** — every color, spacing, radius, shadow, and type scale value comes from a CSS custom property
2. **OKLch for colors** — define colors in `oklch()`; reference them via `var(--ds-*)`; never hardcode bare `oklch()` in component rules
3. **Mobile-first responsive** — design for smallest viewport first, scale up
4. **Accessibility baseline** — WCAG AA; every interactive element has a name, every image has alt text
5. **Progressive enhancement** — components work without JavaScript
6. **Aesthetic judgment** — consider typography, color harmony, spacing rhythm, visual hierarchy as integral to the work, not afterthoughts

## Design Token Reference

### Color Structure

```css
/* Light mode (:root) */
--ds-color-bg:         oklch(97% 0.012 80);
--ds-color-surface:    oklch(99% 0.005 80);
--ds-color-border:     oklch(89% 0.012 80);
--ds-color-fg:         oklch(20% 0.02 60);
--ds-color-accent:     oklch(52% 0.08 115);

/* Dark mode ([data-theme="dark"]) — override every token */
[data-theme="dark"] {
  --ds-color-bg:       oklch(15% 0.008 75);
  --ds-color-surface:  oklch(20% 0.008 75);
  --ds-color-fg:       oklch(84% 0.008 72);
  --ds-color-accent:   oklch(57% 0.065 115);
}
```

### Spacing Scale

Base: 4px. Tokens: `--ds-space-1` (4px) through `--ds-space-32` (128px).

### Typography Scale

```
--ds-font-display: serif stack
--ds-font-body:    sans-serif stack
--ds-font-mono:    monospace stack
```

Type scale (rem): caption .75 · body 1 · h4 1.5 · h3 1.875 · h2 2.25 · h1 3

### Radius Scale

sm: 2px · md: 4px · lg: 8px · xl: 12px · 2xl: 16px

## Common Patterns

### Button

```html
<button class="ds-btn ds-btn--primary" type="button">
  <span class="ds-btn__label">Label</span>
</button>
```

```css
.ds-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--ds-space-2);
  padding: var(--ds-space-2) var(--ds-space-4);
  border-radius: var(--ds-radius-md);
  font: inherit;
  cursor: pointer;
}
.ds-btn--primary {
  background: var(--ds-color-accent);
  color: var(--ds-color-surface-raised);
}
```

Icon-only button requires `aria-label`.

### Card

Base class + modifier pattern. No nested modifier chains like `.parent .child--active`.

### Stack / Cluster Layout

Use layout helper classes. Never use ad-hoc margin tricks.

## Anti-Patterns

| Wrong | Right |
|---|---|
| `color: oklch(52% 0.08 115)` | `color: var(--ds-color-accent)` |
| `padding: 16px` | `padding: var(--ds-space-4)` |
| `<button>icon</button>` | `<button aria-label="Submit form">icon</button>` |
| `<div style="color: #fff">` | class + CSS token |
| No `[data-theme="dark"]` override | override every color token |

## Dark Mode Rules

- Never use pure `#000` — use warm gray `oklch(15% 0.008 75)`
- Dark mode accent is ~5-10% lighter than light mode accent
- Every color token declared in `:root` needs a `[data-theme="dark"]` override

## Pre-Commit Checklist

Before finishing any task:

- [ ] All colors use `var(--ds-*)` tokens, no bare oklch/hex/rgb in component rules
- [ ] All spacing uses `--ds-space-*` tokens, no magic numbers
- [ ] Dark mode overrides exist for every color token
- [ ] Icon-only buttons have `aria-label`
- [ ] Images have `alt` text
- [ ] Semantic HTML (no `<a>` without href in unexpected places)
- [ ] No `inline style=` except for genuinely dynamic values
- [ ] Component is responsive (tested at 375px width)
- [ ] Aesthetic quality: spacing rhythm, typography scale, color harmony checked