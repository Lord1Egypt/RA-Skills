---
name: lemma-widget
description: "Use for inline visual responses in Lemma conversations: diagrams, charts, dashboards, tables, mockups, calculators, and lightweight HTML or SVG widgets rendered with show_widget."
---

# Lemma Widget

Use this skill whenever the assistant should render something visually inline instead of only describing it in prose.

Reading this skill satisfies the widget tool's `read_me` requirement. After reading it, call `show_widget` with `i_have_seen_read_me=true`.

## When To Use This Skill

Use `lemma-widget` when the user would benefit from:

- a diagram
- a chart
- a dashboard summary
- a table or calculator
- a small interactive explainer
- a lightweight mockup

Do not use it for a full application. Use `lemma-desks` for that.
Do not use it for a live running server preview. Use `widget_url` and read `lemma-workspace` for that flow.

## Choose The Right Render Mode

### Use `widget_code`

Use `widget_code` when you are generating the visual directly as HTML or SVG.

### Use `widget_url`

Use `widget_url` when the content is a live HTTP service such as:

- a dev server
- a dashboard running in the workspace
- a browser view via noVNC
- a notebook or other live app

## Choose HTML Versus SVG

### Use SVG when

- the content is a diagram or illustration
- the layout is mostly static
- the visual is about nodes, flows, relationships, or structure

### Use HTML when

- the content is tabular or card-based
- the user needs controls or interactivity
- the output is closer to UI than illustration

## Tool Contract

Call `show_widget` with:

- `i_have_seen_read_me`
- `loading_messages`
- `title`
- exactly one of `widget_code` or `widget_url`

The client auto-detects render mode for `widget_code`:

- code starting with `<svg` renders as SVG
- everything else renders as HTML

## Design Rules

- keep explanation in normal assistant prose outside the tool payload
- keep the widget itself focused on renderable content
- prefer compact layouts over sprawling canvases
- make the widget readable in both light and dark themes
- avoid decorative noise that does not help comprehension

## Theme Tokens

When generating HTML or SVG, prefer platform CSS variables instead of hardcoded styling.
Useful variables include:

- `--color-background-primary`
- `--color-background-secondary`
- `--color-background-tertiary`
- `--color-text-primary`
- `--color-text-secondary`
- `--color-text-tertiary`
- `--color-border-primary`
- `--color-border-secondary`
- `--color-border-tertiary`
- `--font-sans`
- `--font-serif`
- `--font-mono`
- `--border-radius-md`
- `--border-radius-lg`
- `--border-radius-xl`

Use fallbacks when useful, for example:

```html
<div style="color: var(--color-text-primary, #111827);"></div>
```

## Implementation Rules

- do not include `<!DOCTYPE html>`, `<html>`, `<head>`, or `<body>`
- keep external resources limited to approved CDNs when needed
- avoid comments in the widget payload
- avoid tiny text
- keep scripts short and purposeful
- use `sendPrompt(...)` only when a click-through follow-up genuinely helps the user

## Good Defaults

### Diagram widget

Use SVG with a small number of nodes, clear labels, and obvious flow direction.

### Data widget

Use HTML cards or tables with clear labels and restrained styling.

### Interactive explainer

Use HTML with a small number of controls and a clear default state.

## Common Mistakes

- using a widget where a full desk is actually needed
- rendering a live service with `widget_code` instead of `widget_url`
- hardcoding every color instead of using theme tokens
- putting too much explanatory prose inside the widget itself
- making the widget visually busy when the content is simple

## Related Skills

Route to:

- `lemma-workspace` when the result should be a live service preview
- `lemma-desks` when the user needs a real application
- `lemma-main` when the question is about platform design rather than rendering
