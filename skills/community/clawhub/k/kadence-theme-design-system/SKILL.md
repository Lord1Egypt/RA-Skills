---
name: kadence-theme-design-system
description: Use Kadence Theme as a design system for WordPress delivery. Covers design tokens, layout system, header/footer/navigation setup, page/archive/single templates, and a practical Free vs Pro capability matrix so agents choose valid implementations before building.
metadata: {"openclaw":{"emoji":"🎛️"}}
---

# Kadence Theme Design System

Use this skill when working on WordPress sites built with Kadence Theme.

Primary goals:
1. Build and maintain pages/templates with Kadence-native patterns.
2. Keep design decisions tied to global tokens (colors, typography, spacing).
3. Prevent Pro-only feature usage when site only has Free.

## Read Order (important)

1. [references/free-vs-pro-matrix.md](references/free-vs-pro-matrix.md)
2. [references/design-system-foundation.md](references/design-system-foundation.md)
3. [references/elements-and-template-architecture.md](references/elements-and-template-architecture.md)
4. [references/website-management-playbook.md](references/website-management-playbook.md)

## Operating Rules

- Confirm theme/license capability before proposing implementation details.
- Default to **Kadence Free compatible** solutions unless Pro is explicitly confirmed.
- Prefer Gutenberg + Kadence Blocks; avoid custom CSS/JS unless requested.
- Reuse global palette/typography/spacing variables.
- Keep templates editable by non-technical editors.
- For content reads/writes, pair this skill with `wordpress-content-rest-api`.

## Capability Check (before execution)

Do this first in any Kadence task:

1. Verify active theme is Kadence.
2. Verify whether Kadence Pro/Theme Kit Pro features are installed and licensed.
3. Determine feature tier (Free-only vs Free+Pro).
4. Select implementation path from the capability matrix.

If Pro status is unknown, proceed with Free-safe fallback and state the assumption.

## Done Criteria

A Kadence design/system task is complete only when:
- Chosen pattern matches confirmed feature tier.
- Global style tokens are reused (no random hardcoded styling).
- Header/footer/nav/template behavior matches requested UX.
- Any Pro-dependent enhancement is listed separately as optional.
- Editor can maintain the result in Gutenberg without code edits.

## Source Scope

This skill is based on Kadence public docs + help-center pages curated in:
[references/sources.md](references/sources.md)

If docs change, re-check source pages before asserting feature availability.