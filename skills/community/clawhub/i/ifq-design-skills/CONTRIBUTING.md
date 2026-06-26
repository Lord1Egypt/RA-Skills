# Contributing

IFQ Design Skills is optimized for a small, auditable ClawHub bundle and a
template-first design workflow. Contributions should make humans faster and AI
agents more reliable.

## Quality Bar

- Keep the ClawHub bundle zero-install: no new dependencies, no install hooks,
  no hidden network calls, and no background services.
- Prefer clearer routing, better templates, stronger validation, or smaller
  docs over broad rewrites.
- Never add invented facts, fake metrics, fake testimonials, or unlabeled
  placeholder data to examples.
- Preserve China/offline-friendly font fallbacks and local-first behavior.
- Keep IFQ marks ambient in deliverables; do not turn them into loud overlays.

## Before Opening a PR

```bash
npm run validate
npm run pack
```

For template or visual changes, also open the changed HTML in a browser and
record what was checked. For export-helper changes in the full GitHub repo,
verify the actual MP4/GIF/PDF/PPTX file before claiming export support.

## Review Checklist

- The change improves a real user or agent workflow.
- `SKILL.md`, `clawhub.json`, and `assets/templates/INDEX.json` stay aligned.
- References point to files that exist.
- New examples use real facts or labeled placeholders.
- The published bundle remains scanner-friendly and small.
