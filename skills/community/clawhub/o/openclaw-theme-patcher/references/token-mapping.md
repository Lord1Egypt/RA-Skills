# Theme Input → Token Mapping

Use this file when translating a reference theme, screenshot, or palette into OpenClaw Control UI CSS tokens.

## Goal

Map a user's desired theme into a complete and internally consistent token set without changing token names.

## Required output selectors

For a theme id `<theme-id>`:

```css
:root[data-theme=<theme-id>]{...}
:root[data-theme=<theme-id>-light]{...}
```

If the user only wants a dark theme, still prefer drafting a light variant unless they explicitly say dark-only.

## Core mapping

### Background stack

These define the overall depth of the UI.

- `--bg`: main app background
- `--bg-accent`: secondary background zone
- `--bg-elevated`: elevated surface behind panels/dialogs
- `--bg-hover`: hover state on dark/light surfaces
- `--bg-muted`: muted surface fill
- `--panel`: outer panel background
- `--panel-strong`: stronger panel surface
- `--panel-hover`: hovered panel state
- `--card`: card background
- `--popover`: popover / dropdown background
- `--chrome`: top-level chrome with slight transparency
- `--chrome-strong`: stronger chrome layer

Rule:
- keep these in a tight tonal family
- separate them by small but visible steps
- never make `--card`, `--panel`, and `--bg` identical unless the user wants ultra-flat UI

Suggested depth ordering:
- dark: `bg` < `bg-accent/card` < `bg-elevated/panel-strong`
- light: reverse the same logic with lighter surfaces

### Text stack

- `--text`: default text
- `--text-strong`: headings / emphasized text
- `--chat-text`: usually same as `--text`
- `--muted`: secondary text
- `--muted-strong`: stronger secondary text
- `--muted-foreground`: usually same family as `--muted`
- `--card-foreground`: text on cards/popovers
- `--popover-foreground`: text on popovers

Rule:
- `--text-strong` must always be clearly more legible than `--muted`
- do not let muted text get too close to border color

### Border stack

- `--border`: default border
- `--border-strong`: important separators / selected outlines
- `--border-hover`: hovered outline
- `--input`: input border / fill
- `--grid-line`: subtle divider line

Rule:
- in dark themes, borders usually need more contrast than designers first expect
- in light themes, borders should remain visible without turning the UI harsh

### Primary interaction stack

Use the main accent color from the reference theme.

- `--ring`: focus ring source
- `--accent`: primary accent
- `--accent-hover`: hover state of accent
- `--accent-muted`: same hue, lower emphasis
- `--accent-subtle`: low-alpha accent fill
- `--accent-glow`: glow/focus aura
- `--primary`: usually same as accent
- `--primary-foreground`: text on primary buttons
- `--focus`: translucent focus fill

Rule:
- prefer one clear primary accent family
- `--accent-hover` should be a nearby lighter/brighter variant in dark mode, and often slightly darker or richer in light mode

### Secondary accent stack

Use a secondary hue only if the reference theme clearly has one.

- `--accent-2`
- `--accent-2-muted`
- `--accent-2-subtle`

Good sources:
- purple/violet from Tokyo Night
- teal/green from Nord
- mauve/blue from Catppuccin

### State colors

- `--ok`
- `--warn`
- `--danger`
- `--destructive`
- `--info`

Rule:
- keep them readable against the theme background
- do not reuse the primary accent for all states

## Practical extraction order

When deriving from a reference theme, decide in this order:

1. main background
2. elevated/card background
3. default text
4. muted text
5. border family
6. primary accent
7. secondary accent
8. state colors
9. shadows and subtle alpha tokens

## Theme families: common mappings

### Tokyo Night style

Typical anchors:
- background: deep blue-black
- surface: indigo/slate
- text: cool desaturated lavender/blue-gray
- primary accent: blue
- secondary accent: violet
- success: green
- warning: amber
- danger: pink/red

### Nord style

Typical anchors:
- background: cool blue-gray
- surface: slightly lighter steel blue
- text: frosted light gray-blue
- primary accent: icy blue
- secondary accent: teal or muted cyan

### Catppuccin style

Typical anchors:
- background: warm muted dark/light neutrals
- surface: creamy or soft slate layers
- text: soft but clear pastel-tinted neutrals
- primary accent: mauve/blue depending on flavor
- secondary accent: pink/teal/sapphire depending on flavor

## Stability rules

- keep `--ring`, `--accent`, and `--primary` in the same family unless there is a strong reason not to
- keep `--chat-text` aligned with `--text`
- keep `--secondary-foreground` readable on `--secondary`
- keep `--card-foreground` and `--popover-foreground` aligned with the main text stack
- do not invent extra token names

## Fast token checklist

Before finalizing a new theme, check:
- background layers visibly separate
- text is readable on card and panel surfaces
- borders are visible but not louder than text
- accent stands out from info/success/warn/danger
- focus ring is visible on both dark and light variants
- top-right light/dark toggle actually changes the theme variant if both selectors were added
