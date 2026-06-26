# Publish to ClawHub

This skill is structured to be publishable to ClawHub.

## Polished ClawHub listing

- **Name:** `Image to Editable PPT Slide`
- **Slug:** `image-to-editable-ppt-slide`
- **Version:** `1.0.0`
- **Short description:**
  `Rebuild one or more reference images as visually matching editable PowerPoint slides using native shapes, text, fills, and layout instead of a flat screenshot. Use when the user wants an image, flowchart, infographic, dashboard, process diagram, or designed slide converted into an editable PPT/PPTX deck that stays editable and closely matches the source.`
- **Release changelog:**
  `Initial public release with editable single-slide and multi-slide reconstruction workflows, a reusable JSON-to-PPTX builder, and a starter spec generator for turning reference images into matching editable PowerPoint decks.`

## Preflight

Make sure the `clawhub` CLI is installed and authenticated:

```bash
clawhub whoami
```

If not logged in:

```bash
clawhub login
clawhub whoami
```

## Publish command

Run from the workspace root:

```bash
clawhub publish ./skills/image-to-editable-ppt-slide \
  --slug image-to-editable-ppt-slide \
  --name "Image to Editable PPT Slide" \
  --version 1.0.0 \
  --changelog "Initial public release with editable single-slide and multi-slide reconstruction workflows, a reusable JSON-to-PPTX builder, and a starter spec generator for turning reference images into matching editable PowerPoint decks."
```

## Longer release notes source

See `CHANGELOG.md` for the fuller v1.0.0 release notes.

## Suggested future versions

- `1.0.1` – small documentation fixes and better examples
- `1.1.0` – new supported shapes and layout helpers
- `2.0.0` – spec format breaking changes

## Notes

- Publishing writes externally to ClawHub, so only do it when explicitly requested.
- If publish fails due to auth, complete `clawhub login` first.
