# Variables and Design Tokens

> **Applies to**: Mode A (Direct File Writing) + Mode B (MCP Tools)
> **See also**: [codegen-mapping.md](codegen-mapping.md) · [codegen-workflow.md](codegen-workflow.md)

---

## Core Principle: Variables Are Contracts

> **Inspired by Stitch** — Stitch treats design tokens as the design system's "contract": colors, radii, and fonts are all bound through named variables, not isolated magic numbers. The essence of `DESIGN.md` is making these contracts machine-readable so AI can strictly enforce them when generating UI.

Hardcoded values (`fill: "#3b82f6"`, `cornerRadius: 8`) will:

- Force code generation to emit arbitrary values like `bg-[#3b82f6]`, making theming impossible
- Break dark mode (values don't adapt to theme changes)
- Require manual find-and-replace for global design system updates
- Disconnect the design from the codebase's token system

---

## Workflow: Read and Apply Variables

### Step 1 — Read All Variables (MCP Mode)

**Before starting any design task**:

```
pencil_get_variables({ filePath: "path/to/file.pen" })
```

Example output:

```json
{
  "variables": {
    "primary":    { "value": "#3b82f6" },
    "background": { "value": "#ffffff" },
    "foreground": { "value": "#0a0a0a" },
    "border":     { "value": "#e2e8f0" },
    "radius-md":  { "value": 6 }
  }
}
```

### Step 2 — Map Values to Variables

| Style needed | ❌ Don't use | ✅ Use variable instead |
|-------------|-------------|------------------------|
| Brand blue | `fill: "#3b82f6"` | `fill: "$--primary"` |
| White text on primary | `fill: "#ffffff"` | `fill: "$--primary-foreground"` |
| Border color | `stroke.fill: "#e2e8f0"` | `stroke.fill: "$--border"` |
| Medium radius | `cornerRadius: 6` | `cornerRadius: "$--radius-md"` |
| Page background | `fill: "#ffffff"` | `fill: "$--background"` |
| Body text color | `fill: "#0a0a0a"` | `fill: "$--foreground"` |

### Step 3 — Apply Variables in .pen Files

Variable reference syntax: prefix the variable name with `$`:

```json
{
  "fill": "$--background",
  "stroke": { "fill": "$--border" },
  "cornerRadius": "$--radius-md",
  "fontFamily": "$--font-primary"
}
```

Supported on: `fill`, `stroke.fill`, `cornerRadius`, `fontFamily`

### Step 4 — Create Missing Variables

If a needed token doesn't exist, create it immediately — **never hardcode**:

```
pencil_set_variables({
  filePath: "path/to/file.pen",
  variables: {
    "accent":            { "value": "#f59e0b" },
    "accent-foreground": { "value": "#ffffff" }
  }
})
```

---

## Theme Support (Multi-Value Variables)

Variables can hold different values per theme:

```json
{
  "--background": {
    "type": "color",
    "value": [
      { "value": "#fafafa" },
      { "value": "#09090b", "theme": { "Mode": "Dark" } }
    ]
  }
}
```

With themed variables, designs automatically adapt when switching themes. Hardcoded values completely break this mechanism.

---

## Variable-to-Code Mapping (Tailwind v4 + shadcn/ui)

> **Inspired by Stitch cross-tool interoperability** — Design tokens should not be locked inside the design tool. They should flow into code. Pencil variables map directly to Tailwind `@theme` declarations and semantic utility classes.

### Color Token Mapping

| Pencil Variable | `@theme` Declaration | Tailwind Utility |
|----------------|---------------------|-----------------|
| `primary` | `--color-primary` | `bg-primary` / `text-primary` / `border-primary` |
| `primary-foreground` | `--color-primary-foreground` | `text-primary-foreground` |
| `secondary` | `--color-secondary` | `bg-secondary` / `text-secondary` |
| `secondary-foreground` | `--color-secondary-foreground` | `text-secondary-foreground` |
| `background` | `--color-background` | `bg-background` |
| `foreground` | `--color-foreground` | `text-foreground` |
| `muted` | `--color-muted` | `bg-muted` |
| `muted-foreground` | `--color-muted-foreground` | `text-muted-foreground` |
| `accent` | `--color-accent` | `bg-accent` |
| `accent-foreground` | `--color-accent-foreground` | `text-accent-foreground` |
| `destructive` | `--color-destructive` | `bg-destructive` / `text-destructive` |
| `card` | `--color-card` | `bg-card` |
| `card-foreground` | `--color-card-foreground` | `text-card-foreground` |
| `border` | `--color-border` | `border-border` |
| `ring` | `--color-ring` | `ring-ring` |

### Radius Token Mapping

| Pencil Variable | `@theme` Declaration | Tailwind Utility |
|----------------|---------------------|-----------------|
| `radius-sm` | `--radius-sm: 0.25rem` | `rounded-sm` |
| `radius-md` | `--radius-md: 0.375rem` | `rounded-md` |
| `radius-lg` | `--radius-lg: 0.5rem` | `rounded-lg` |
| `radius-xl` | `--radius-xl: 0.75rem` | `rounded-xl` |

### Code Generation: No Arbitrary Values

The rule is simple: **if a Pencil variable exists for a value, there is a corresponding semantic utility. Use the utility, not arbitrary syntax.**

| ❌ Wrong (arbitrary) | ✅ Correct (semantic utility) |
|---------------------|------------------------------|
| `bg-[#3b82f6]` | `bg-primary` |
| `text-[#ffffff]` | `text-primary-foreground` |
| `text-[var(--primary)]` | `text-primary` |
| `rounded-[6px]` | `rounded-md` |
| `border-[#e2e8f0]` | `border-border` |

### Opacity Modifiers

```
bg-primary/90       → primary color at 90% opacity
text-foreground/70  → foreground color at 70% opacity
border-border/50    → border color at 50% opacity
```

Use these instead of arbitrary `opacity` values or `color-mix()`.

---

## Variable Categories Quick Reference

| Category | Common Variable Names | Tailwind Prefix |
|----------|----------------------|----------------|
| Brand colors | `primary`, `secondary`, `accent` | `--color-*` |
| Semantic colors | `destructive`, `success`, `warning`, `info` | `--color-*` |
| Surface colors | `background`, `foreground`, `card`, `card-foreground` | `--color-*` |
| UI colors | `border`, `ring`, `muted`, `muted-foreground` | `--color-*` |
| Border radius | `radius-sm/md/lg/xl` | `--radius-*` |
| Typography | `font-sans`, `font-mono`, `font-heading` | `--font-*` |
| Spacing | `spacing-xs/sm/md/lg` | `--spacing-*` |

---

## Pre-Application Checklist

- [ ] Ran `pencil_get_variables` to see available tokens?
- [ ] All colors using variable references instead of hardcoded hex?
- [ ] All radii using variable references instead of hardcoded pixel values?
- [ ] Missing variables created with `pencil_set_variables`?
- [ ] Code generation outputs semantic utilities (`bg-primary`) not arbitrary values (`bg-[#3b82f6]`)?

---

## See Also

- [codegen-mapping.md](codegen-mapping.md) — Complete quick-reference mapping tables
- [codegen-workflow.md](codegen-workflow.md) — Complete code generation workflow using tokens
- [responsive.md](responsive.md) — Breakpoint tokens and responsive patterns
