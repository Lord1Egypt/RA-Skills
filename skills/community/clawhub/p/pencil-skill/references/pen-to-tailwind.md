# .pen → Tailwind CSS Conversion Table

Use this when converting `.pen` designs into React/Tailwind code.

## Node → HTML Mapping

| .pen Node | HTML/React |
|-----------|------------|
| `frame` (layout) | `<div className="flex gap-4 p-6">` |
| `text` | `<p>`, `<h1-6>`, `<span>` |
| `rectangle` | `<div>` with background |
| `ellipse` | `<div className="rounded-full">` |
| `ref` (instance) | Reusable React component |
| `icon_font` | Icon component |

## Layout

| .pen | Tailwind |
|------|----------|
| `layout: "vertical"` | `flex flex-col` |
| `layout: "horizontal"` | `flex flex-row` |
| `layout: "none"` | `relative` (absolute positioning) |
| `alignItems: "center"` | `items-center` |
| `alignItems: "start"` | `items-start` |
| `alignItems: "end"` | `items-end` |
| `justifyContent: "center"` | `justify-center` |
| `justifyContent: "start"` | `justify-start` |
| `justifyContent: "end"` | `justify-end` |
| `justifyContent: "space_between"` | `justify-between` |
| `justifyContent: "space_around"` | `justify-around` |

## Spacing (8pt grid)

| .pen gap | Tailwind |
|----------|----------|
| 4 | `gap-1` |
| 8 | `gap-2` |
| 12 | `gap-3` |
| 16 | `gap-4` |
| 20 | `gap-5` |
| 24 | `gap-6` |
| 32 | `gap-8` |
| 48 | `gap-12` |

| .pen padding | Tailwind |
|-------------|----------|
| `[8,8,8,8]` | `p-2` |
| `[16,16,16,16]` | `p-4` |
| `[16,24,16,24]` | `py-4 px-6` |
| `[24,32,24,32]` | `py-6 px-8` |

## Sizing

| .pen | Tailwind |
|------|----------|
| `"fill_container"` | `w-full` / `h-full` |
| `"fit_content"` | `w-fit` / `h-fit` |
| number (px) | `w-[Npx]` / `h-[Npx]` |

## Typography

| .pen fontSize | Tailwind |
|--------------|----------|
| 12 | `text-xs` |
| 14 | `text-sm` |
| 16 | `text-base` |
| 18 | `text-lg` |
| 20 | `text-xl` |
| 24 | `text-2xl` |
| 30 | `text-3xl` |
| 36 | `text-4xl` |
| 48 | `text-5xl` |

| .pen fontWeight | Tailwind |
|----------------|----------|
| 300 | `font-light` |
| 400 | `font-normal` |
| 500 | `font-medium` |
| 600 | `font-semibold` |
| 700 | `font-bold` |
| 800 | `font-extrabold` |

## Colors

Variables → Tailwind theme:

```css
@theme {
  --color-primary: var(--pen-color-primary);
  --color-surface: var(--pen-color-surface);
  --color-foreground: var(--pen-color-foreground);
}
```

Usage: `bg-primary`, `text-foreground`, `border-surface`

**Strictly prohibited:** arbitrary values like `bg-[#3b82f6]`, `text-[var(--primary)]`

## Border Radius

| .pen cornerRadius | Tailwind |
|------------------|----------|
| `[0,0,0,0]` | `rounded-none` |
| `[2,2,2,2]` | `rounded-sm` |
| `[4,4,4,4]` | `rounded` |
| `[6,6,6,6]` | `rounded-md` |
| `[8,8,8,8]` | `rounded-lg` |
| `[12,12,12,12]` | `rounded-xl` |
| `[16,16,16,16]` | `rounded-2xl` |
| `[9999,9999,9999,9999]` | `rounded-full` |

## Effects

| .pen effect | Tailwind |
|-------------|----------|
| `shadow` (small) | `shadow-sm` |
| `shadow` (medium) | `shadow-md` |
| `shadow` (large) | `shadow-lg` |
| `blur` | `blur-sm` / `blur-md` / `blur-lg` |
| `background_blur` | `backdrop-blur-sm` / `backdrop-blur-md` |