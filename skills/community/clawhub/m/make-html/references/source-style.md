# Source Style

When an artifact explains or represents an existing project, product, app, docs site, or brand, inspect that source's styling before designing the page.

Source style has priority over saved custom themes. Use a saved theme only when the user explicitly asks to override source style, or when no usable source style exists.

## Style Provenance Gate

Before writing CSS, choose exactly one style source:

- **Source-backed style**: use this only after inspecting concrete style evidence such as CSS variables, theme config, UI component source, local screenshots, product pages, or docs CSS.
- **Saved theme**: use only when the user names one, asks for a saved/default theme, or a saved theme clearly matches after source style is unavailable.
- **Fallback theme**: use `themes/fallback-theme.md` when no concrete source style or saved theme applies.

Do not infer style from source content, project subject matter, docs prose, CLI output, or the model's memory of the product. Reading repository files for facts is not enough to claim source style. If style evidence is missing, say so briefly inside the artifact and use the fallback theme.

Every artifact about an existing project, product, app, docs site, or brand must include a compact style provenance note. Put it in a footer, source/evidence panel, or metadata row. It should name either the inspected style files/tokens, the saved theme file, or `themes/fallback-theme.md`.

## What To Inspect

Look for these files first, using the names that fit the project:

- `styles.css`, `globals.css`, `global.css`, `base.css`, `components.css`
- `tailwind.config.*`, theme config, token JSON, design token files
- UI component source for buttons, chips, cards, tabs, nav, tables, and status badges
- docs custom CSS
- existing screenshots or product pages if available locally
- built app assets such as `dist/**/index.html` and compiled CSS when source CSS is not available

Search terms that usually find the useful pieces:

- `--accent`, `--primary`, `--bg`, `--card`, `--border`, `--muted`, `--radius`, `--shadow`
- `chip`, `pill`, `badge`, `btn`, `card`, `nav`, `toolbar`, `status`
- `font-family`, `color-scheme`, `theme`, `data-theme`

## How To Apply It

- Reuse the product's tokens where possible instead of inventing a new palette.
- If a product has an app/control UI and docs, choose the surface most relevant to the artifact. For an operational/product-system artifact, prefer app/control UI tokens over README or generic docs styling.
- Match the product's density. Operational dashboards should feel compact and work-focused; docs pages can be more spacious; marketing pages can be more expressive.
- Preserve recognizability: accent color, secondary accent, surface depth, radius, borders, focus treatment, button/chip style, typography, and motion.
- Avoid blindly copying a whole app shell when the artifact is a standalone report. Borrow the flavor and components, then design the artifact for its job.
- If the project has multiple themes, choose the one most recognizable or relevant to the artifact and note the source.
- Include style evidence in the artifact when the styling is a meaningful requirement: token names, file paths, and a short explanation of what was reused.
- If the artifact uses source-backed style, the CSS should visibly reflect the extracted tokens. A source-backed artifact should not look like a generic neutral dashboard unless the source style itself does.

## Common Misses

- Creating a neutral gray dashboard when the source app has strong theme tokens.
- Treating source code or docs content as style evidence without inspecting UI CSS, token files, component source, screenshots, or product pages.
- Falling back to a model-invented light admin palette instead of `themes/fallback-theme.md`.
- Using horizontal scrolling for chip-like controls because the source app has dense controls elsewhere.
- Copying colors but missing the source density, borders, radius, and button states.
- Adding every possible relationship to a diagram even when the source project favors compact, readable operational UI.
