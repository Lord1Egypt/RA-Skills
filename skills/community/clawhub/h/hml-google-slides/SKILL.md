---
name: google-slides
description: "Create, edit, and export Google Slides presentations. Use when creating new presentations, adding or updating slides, reading slide content, exporting to PDF/PPTX, or building a deck from scratch. Requires gog auth to be working."
---

# Google Slides

Uses the `gog` CLI for basic operations and `scripts/slides.py` for advanced edits (adding/editing slide content via the Slides API).

## Auth Check

Before any Slides operation, verify auth is working:
```bash
gog slides info <any-presentation-id> --account david@hml.tech
```
If it fails, re-auth: `gog auth add david@hml.tech --services gmail,calendar,drive,docs,sheets,contacts,tasks,people`

## Core Commands (via gog)

```bash
# Create a new blank presentation
gog slides create "My Presentation" --account david@hml.tech --json

# Get info about a presentation (slide count, title, etc.)
gog slides info <presentationId> --account david@hml.tech --json

# Export to PDF
gog slides export <presentationId> --format pdf --out /tmp/deck.pdf --account david@hml.tech

# Export to PPTX
gog slides export <presentationId> --format pptx --out /tmp/deck.pptx --account david@hml.tech

# Copy a presentation (e.g., to use a template)
gog slides copy <presentationId> "Copy Title" --account david@hml.tech --json
```

## Adding/Editing Slide Content (via scripts/slides.py)

For adding text slides, batch updates, and reading full content, use `scripts/slides.py`.

```bash
# Add a text slide with title and bullet body
python3 scripts/slides.py add-slide <presentationId> \
  --title "Slide Title" \
  --body "• Bullet point one\n• Bullet point two"

# Add a slide at a specific position (0-indexed)
python3 scripts/slides.py add-slide <presentationId> --title "Intro" --insert-at 0

# Run arbitrary batch update requests from a JSON file
python3 scripts/slides.py batch <presentationId> requests.json

# Export via script
python3 scripts/slides.py export <presentationId> --format pdf --out /tmp/deck.pdf

# List comments with their anchors (e.g. which slide they are on)
python3 scripts/slides.py list-comments <presentationId>

# Resolve a comment and optionally leave a reply message
python3 scripts/slides.py resolve-comment <presentationId> <commentId> --reply "Fixed!"
```

## Building a Deck from Scratch

Typical workflow:
1. Create presentation: `gog slides create "Title" --json` → get `presentationId`
2. Add slides one by one using `scripts/slides.py add-slide`
3. For rich content (images, shapes, formatting), write batch requests to a JSON file and run `scripts/slides.py batch`
4. Export: `gog slides export <id> --format pdf --out /tmp/deck.pdf`

For complex batch requests (images, shapes, text formatting), see `references/batch_requests.md`.

## Getting Presentation ID

From a Google Slides URL:
`https://docs.google.com/presentation/d/**<presentationId>**/edit`

## Notes

- `gog slides` uses the Drive API under the hood (no separate Slides scope needed)
- `scripts/slides.py` uses the Google Slides API directly and requires working gog auth tokens
- Set `GOG_ACCOUNT=david@hml.tech` in env to skip `--account` flag
