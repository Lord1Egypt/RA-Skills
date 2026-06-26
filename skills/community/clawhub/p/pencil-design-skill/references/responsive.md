# Responsive Breakpoints

> **Applies to**: Mode A (Direct File Writing) + Mode B (MCP Tools)
> **See also**: [overflow-prevention.md](overflow-prevention.md) · [codegen-workflow.md](codegen-workflow.md)

---

## Artboard Size → Tailwind Breakpoint Mapping

### Standard Artboard Width Reference

| Device | Pencil Artboard Width | Tailwind Breakpoint | Prefix |
|--------|----------------------|--------------------|----|
| Mobile (small) | 320px | Default (no prefix) | — |
| Mobile (standard) | 375px | Default (no prefix) | — |
| Mobile (large) | 393–430px | Default (no prefix) | — |
| Tablet (portrait) | 768px | `md` | `md:` |
| Tablet (landscape) | 1024px | `lg` | `lg:` |
| Desktop | 1280px | `xl` | `xl:` |
| Desktop (wide) | 1440px | `2xl` | `2xl:` |
| Desktop (ultrawide) | 1920px | `2xl` or custom | `2xl:` |

### Tailwind v4 Built-in Breakpoint Values

```css
/* Built into Tailwind — no @theme declaration needed */
sm  →  640px
md  →  768px
lg  →  1024px
xl  →  1280px
2xl →  1536px
```

Custom breakpoints (Tailwind v4):

```css
@theme {
  --breakpoint-xs: 475px;
  --breakpoint-3xl: 1920px;
}
```

---

## Multi-Artboard Design → Code Generation Strategy

### Reading All Artboards

```
pencil_batch_get({
  filePath: "path/to/file.pen",
  patterns: [{ type: "frame", name: "Mobile|Tablet|Desktop" }],
  readDepth: 4
})
```

Or read top-level nodes directly:

```
pencil_batch_get({ filePath: "path/to/file.pen" })
```

### Mobile-First Code Generation

Use the smallest artboard (mobile) as base styles, then layer breakpoint overrides for larger sizes:

```tsx
// base styles = mobile artboard
// md: styles = tablet artboard
// lg: styles = desktop artboard

<div className="flex flex-col gap-4 p-4 md:flex-row md:gap-6 md:p-6 lg:gap-8 lg:p-8">
  {/* Sidebar: stacks on mobile, side-by-side on tablet+ */}
  <aside className="w-full md:w-64 lg:w-72">
    {/* ... */}
  </aside>

  {/* Main content: full-width on mobile, flexible on tablet+ */}
  <main className="flex-1">
    {/* ... */}
  </main>
</div>
```

---

## Common Responsive Patterns

| Pencil Design Pattern | Tailwind Implementation |
|----------------------|------------------------|
| 1 column (mobile) → 2 columns (tablet) → 3 columns (desktop) | `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3` |
| Stacked sidebar (mobile) → side-by-side (desktop) | `flex flex-col lg:flex-row` |
| Hidden on mobile, visible on desktop | `hidden lg:block` |
| Visible on mobile, hidden on desktop | `block lg:hidden` |
| Full-width mobile, constrained desktop | `w-full max-w-7xl mx-auto` |
| Small text mobile, larger desktop | `text-sm md:text-base lg:text-lg` |
| Less padding mobile, more padding desktop | `p-4 md:p-6 lg:p-8` |
| Card grid 1/2/3 columns | `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6` |
| Mobile hamburger menu → desktop full nav | Mobile: `<Sheet>` / Desktop: `<nav className="hidden md:flex">` |

---

## Artboard Diff Quick Reference

When comparing mobile vs. desktop artboards, focus on these changes:

| What Changes | Mobile Artboard | Desktop Artboard | Code Pattern |
|-------------|----------------|-----------------|--------------|
| Layout direction | `layout: "vertical"` | `layout: "horizontal"` | `flex flex-col lg:flex-row` |
| Column count | 1 column | 2–4 columns | `grid-cols-1 lg:grid-cols-3` |
| Visibility | Element absent | Element present | `hidden lg:block` |
| Font size | Smaller | Larger | `text-2xl lg:text-4xl` |
| Padding | 16px | 24–32px | `p-4 lg:p-8` |
| Gap | 16px | 24px | `gap-4 lg:gap-6` |
| Sidebar | Hidden or stacked | Side-by-side | `hidden lg:block lg:w-64` |
| Image size | Smaller/cropped | Full size | `h-48 lg:h-80` |

---

## Container Queries (Advanced)

When a component needs to respond to its **parent container** width (not the viewport):

```tsx
<div className="@container">
  <div className="flex flex-col @md:flex-row @lg:gap-8">
    {/* Responds to parent container width, not viewport */}
  </div>
</div>
```

Use when the same component appears in different contexts (sidebar vs. main content) and must adapt accordingly.

---

## Anti-Patterns

| ❌ Wrong | ✅ Correct |
|---------|----------|
| Hardcoding artboard pixel widths into code | Use Tailwind breakpoints + responsive utilities |
| Writing separate mobile/desktop components | One component with responsive classes |
| Using `max-width` media queries | Mobile-first `min-width` (Tailwind default) |
| Ignoring the mobile artboard | Always start from mobile, add `md:` / `lg:` |
| Writing `@media` in CSS for breakpoints | Use Tailwind responsive prefixes in className |
| `w-[375px]` from mobile artboard | `w-full` with responsive max-width |
| `w-[1440px]` from desktop artboard | `max-w-7xl mx-auto` or similar |

---

## Code Generation Checklist

- [ ] Identified all artboard sizes and mapped them to Tailwind breakpoints?
- [ ] Generating mobile-first code (base styles = mobile artboard)?
- [ ] Tablet/desktop differences use breakpoint prefixes (`md:`, `lg:`)?
- [ ] Compared artboards to find what changes between sizes?
- [ ] Column count changes use `grid-cols-*` with breakpoint prefixes?
- [ ] Visibility changes use `hidden` / `block` with breakpoint prefixes?
- [ ] No hardcoded artboard pixel dimensions in class names?

---

## See Also

- [overflow-prevention.md](overflow-prevention.md) — Overflow prevention and mobile layout rules
- [codegen-workflow.md](codegen-workflow.md) — Complete code generation workflow
- [codegen-mapping.md](codegen-mapping.md) — Property-to-Tailwind class quick reference
