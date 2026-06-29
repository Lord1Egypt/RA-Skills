# Custom Themes

Custom themes let users save reusable visual guidance inside the installed skill folder.

Theme files live in:

```text
themes/*.md
```

Use this reference when the user asks for a saved, custom, personal, house, or named theme, or when no source/project style exists and a theme in `themes/` is marked as the default.

Ignore `themes/theme-template.md` and `themes/fallback-theme.md` when selecting a saved user theme. The template is only a scaffold, and the fallback theme is the final built-in default.

## Lookup Order

1. Source style from the target project, product, brand, app, or docs still wins.
2. If the user names a saved theme, read the matching `themes/<name>.md` file and apply it.
3. If the user asks for their custom/default theme without naming one, inspect `themes/*.md` except `theme-template.md` and `fallback-theme.md` and choose the file with `default: true`.
4. If no default exists, choose a theme whose `tags` or description clearly match the task.
5. If no saved theme clearly applies, use `themes/fallback-theme.md`.

Never create an unnamed theme between these steps. If source style is not backed by concrete evidence and no saved theme applies, the fallback theme is mandatory.

Do not ask the user to choose a theme unless several saved themes are equally plausible and the style choice matters.

## Theme File Format

Themes are plain Markdown with optional YAML frontmatter:

````markdown
---
name: calm-ops
description: Compact operational dashboard theme for status pages and internal tools.
tags: dashboard, status, incident, ops
default: false
---

# Calm Ops

## Use When

- Internal dashboards, incident reports, status pages, and triage surfaces.

## Tokens

```css
:root {
  --bg: #F7F8F4;
  --paper: #FFFFFF;
  --ink: #17201A;
  --muted: #667064;
  --line: #D7DDCF;
  --accent: #4F7F62;
}
```

## Typography

- System sans body, compact mono labels, no viewport-sized text.

## Components

- Dense cards, thin borders, compact status chips, visible focus states.

## Avoid

- Decorative gradients, oversized cards, horizontal chip scrolling.
````

Required content:

- `name`
- `description`
- `tags`
- tokens or a clear palette
- typography guidance
- component guidance
- avoid list

Optional content:

- `default: true` to make the theme the preferred saved theme when no source style exists.
- example CSS snippets for cards, nav, code blocks, diagrams, and charts.
- sample component states.

## Applying A Theme

- Keep the artifact self-contained. Inline any CSS from the theme in the generated HTML.
- Translate theme guidance into the artifact's actual shape. Do not copy irrelevant app chrome.
- Preserve universal `make-html` rules: wrapped chips, real selected states, bounded diagram overflow, responsive layout, accessible controls, and browser validation.
- If a theme conflicts with source/project style, prefer source/project style unless the user explicitly asks to override it.
- If a theme omits a component pattern needed by the artifact, combine the theme tokens with the corresponding `make-html` reference pattern.
- Include a compact style provenance note naming the theme file used.

## Saving A New Theme

When the user asks to save the current styling as a reusable theme:

1. Create `themes/<slug>.md` in the installed skill folder.
2. Include frontmatter with `name`, `description`, `tags`, and `default`.
3. Extract the actual reusable choices: tokens, typography, layout density, border/radius/shadow rules, control states, code example styling, diagram styling, and avoid list.
4. Keep project-specific names, data, routes, and screenshots out of the theme unless the user is intentionally saving a brand theme.
5. Tell the user the saved theme path and the phrase they can use later, for example: "use the calm-ops theme."

Theme files are user-owned. Do not overwrite an existing theme with the same slug unless the user explicitly asks to update it.
