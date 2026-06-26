# Design-to-Code Workflow

> Read this when generating code from a `.pen` file.
> Companion: [`codegen-mapping.md`](codegen-mapping.md) (quick mapping tables) · [`design-tokens.md`](design-tokens.md) · [`responsive.md`](responsive.md).

## Target Stack

React / Next.js · TypeScript · **Tailwind CSS v4** · shadcn/ui · Lucide Icons · CVA + `cn()`.

## Workflow (7 steps)

```
1. Load `frontend-design` skill        (MANDATORY — aesthetic direction)
2. pencil_get_guidelines topic=code|tailwind   (Mode B)
3. pencil_get_variables                (read tokens → @theme)
4. pencil_batch_get tree               (read design hierarchy)
5. pencil_batch_get reusable=true      (find components for shadcn mapping)
6. Generate code (CSS @theme + components + page)
7. (Optional) pencil_set_variables     (sync token changes back)
```

## Step 3 — Variable → Tailwind utility (1:1)

| Pencil variable | `@theme` declaration | Utility |
|----------------|---------------------|---------|
| `--background` | `--color-background` | `bg-background` |
| `--foreground` | `--color-foreground` | `text-foreground` |
| `--primary` | `--color-primary` | `bg-primary` |
| `--primary-foreground` | `--color-primary-foreground` | `text-primary-foreground` |
| `--muted` / `--muted-foreground` | `--color-muted` / `--color-muted-foreground` | `bg-muted` / `text-muted-foreground` |
| `--border` | `--color-border` | `border-border` |
| `--ring` | `--color-ring` | `ring-ring` |
| `--radius-md` | `--radius-md` | `rounded-md` |

**Prefix rules**: colors MUST use `--color-*`, radii MUST use `--radius-*`. Tailwind v4 auto-generates utilities from these prefixes.

Full token mapping: [`design-tokens.md`](design-tokens.md).

## Step 5 — Component mapping (Pencil → shadcn/ui)

| Pencil name (any of) | shadcn component | Import |
|---|---|---|
| Button / Btn | `<Button>` | `@/components/ui/button` |
| Card / Tile / Panel | `<Card>` + `<CardHeader>` `<CardContent>` `<CardFooter>` | `@/components/ui/card` |
| Input / TextField | `<Input>` | `@/components/ui/input` |
| Select / Dropdown | `<Select>` + Trigger/Content/Item | `@/components/ui/select` |
| Checkbox / Switch | `<Checkbox>` / `<Switch>` | matching path |
| Badge / Tag / Chip | `<Badge>` | `@/components/ui/badge` |
| Avatar | `<Avatar>` + Image/Fallback | `@/components/ui/avatar` |
| Dialog / Modal | `<Dialog>` + Trigger/Content | `@/components/ui/dialog` |
| Tabs / TabBar | `<Tabs>` + List/Trigger/Content | `@/components/ui/tabs` |
| Table / DataTable | `<Table>` + Header/Row/Cell | `@/components/ui/table` |
| Tooltip · Label · Separator | matching shadcn primitive | matching path |

For unmatched components: build with **CVA + `cn()` + React 19 ref-as-prop** (same conventions as shadcn primitives).

If unsure whether a shadcn component exists, query the registry:
```
shadcn_search_items_in_registries({ registries: ["@shadcn"], query: "data table" })
shadcn_view_items_in_registries({ items: ["@shadcn/data-table"] })
```

## Step 6 — Code patterns

### CSS setup (`app.css` / `globals.css`)

```css
@import "tailwindcss";

@theme {
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);
  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);
  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);
  --color-border: oklch(91% 0.01 264);
  /* ... other --color-* and --radius-* tokens */

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}

@custom-variant dark (&:where(.dark, .dark *));

.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);
  /* ... dark overrides */
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground antialiased; }
}
```

Rules: (1) prefer OKLCH (convert hex if needed), (2) prefixes are required, (3) NO `tailwind.config.ts` in v4.

### Custom component (CVA pattern)

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const statusBadge = cva(
  "inline-flex items-center rounded-md px-2 py-1 text-xs font-medium",
  {
    variants: {
      status: {
        active:   "bg-primary text-primary-foreground",
        inactive: "bg-muted text-muted-foreground",
        error:    "bg-destructive text-destructive-foreground",
      },
    },
    defaultVariants: { status: "active" },
  }
)

interface Props
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadge> {}

export function StatusBadge({ className, status, ...props }: Props) {
  return <span className={cn(statusBadge({ status, className }))} {...props} />
}
```

Note: semantic classes only · React 19 (no `forwardRef`) · `cn()` for merging.

### `lib/utils.ts` (must exist)

```ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

## Responsive (multi-artboard)

When the `.pen` file has artboards at multiple widths (375 / 768 / 1280 etc.):

1. Read all artboards, compare structure
2. Generate **mobile-first** (base = smallest artboard)
3. Use `md:` `lg:` `xl:` to override
4. **Never hardcode artboard widths** — use `w-full`, `max-w-7xl mx-auto`, responsive grid columns

Full breakpoint mapping: [`responsive.md`](responsive.md).

## Layout property mapping (essentials)

| Pencil | Tailwind |
|---|---|
| `layout: "vertical"` | `flex flex-col` |
| `layout: "horizontal"` | `flex` |
| `gap: 16` / `24` | `gap-4` / `gap-6` |
| `padding: 16` / `24` | `p-4` / `p-6` |
| `width: "fill_container"` | `w-full` or `flex-1` |
| `alignItems: "center"` | `items-center` |
| `justifyContent: "space_between"` | `justify-between` |

Full mapping: [`codegen-mapping.md`](codegen-mapping.md).

## Icon mapping (Material → Lucide, common)

`search→Search` · `close→X` · `menu→Menu` · `arrow_forward→ArrowRight` · `arrow_back→ArrowLeft` · `person→User` · `settings→Settings` · `home→Home` · `notifications→Bell` · `edit→Pencil` · `delete→Trash2` · `add→Plus` · `check→Check` · `visibility→Eye` · `visibility_off→EyeOff` · `chevron_right→ChevronRight` · `chevron_down→ChevronDown` · `more_vert→MoreVertical` · `more_horiz→MoreHorizontal` · `mail→Mail` · `calendar_today→Calendar` · `favorite→Heart` · `star→Star` · `download→Download` · `upload→Upload` · `filter_list→Filter` · `sort→ArrowUpDown` · `logout→LogOut`.

Pencil files use `iconFontFamily: "lucide"` directly — names usually match Lucide kebab-case (`folder-open`, `chevron-down`).

## Rules Summary

✓ Load `frontend-design` skill · semantic Tailwind utilities only · `--color-*` / `--radius-*` prefixes · OKLCH preferred · CVA + `cn()` · React 19 (`ref` as prop) · TypeScript · Lucide icons · mobile-first · split files for multi-component screens.

✗ Arbitrary values (`bg-[#fff]`, `rounded-[6px]`, `p-[24px]`, `text-[14px]`) · `tailwind.config.ts` · `@tailwind base/components/utilities` · `forwardRef` · monolithic single-file pages · hardcoded artboard widths (`w-[375px]`).
