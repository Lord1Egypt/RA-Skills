---
name: macaron-card-generator
description: Generate beautiful macaron-color cartoon illustration-style card images from text content. Supports various types such as book recommendation cards, concept cards, quote cards, and comparison cards, with multiple aspect ratios including 3:4, 9:16, and 1:1.
---

# Macaron Card Generator

Generate beautiful card images from text content with one click, in a macaron-color cartoon illustration style.

## Trigger Words

Generate card, make a card, draw a card, generate image, book card, recommendation card, concept card, quote card, comparison card, create an image.

## Workflow

1. Understand user requirements → Confirm card type, content, and aspect ratio
2. Construct JSON content → Organize data by card type (see references/design_guide.md for field descriptions)
3. Run `scripts/generate_card.py` → Generate HTML file
4. Screenshot with Playwright/CDP → Render HTML as PNG
5. Send PNG to user

## Quick Start

```powershell
python scripts/generate_card.py \
  --type book \
  --content '{"title":"The Little Prince","author":"Antoine de Saint-Exupéry","recommendation_reason":"...","key_takeaway":"...","rating":"5","tags":["Classic"],"ratio":"3:4"}' \
  --output card.html
```

Then render `card.html` as a PNG using a browser screenshot tool.

## Card Types

| Type | --type | Description |
|------|--------|-------------|
| Book Recommendation Card | `book` | Title, author, rating, recommendation reason, quote tags |
| Concept Card | `concept` | Concept name, definition, examples, related concepts |
| Quote Card | `quote` | Quoted text, author, source, background |
| Comparison Card | `compare` | Comparison topic, characteristics of both sides, conclusion |

## Design System

All cards follow the macaron-color cartoon illustration style:
- Soft pastel gradient backgrounds + white rounded card
- Dashed double borders simulating a hand-drawn feel
- Decorative circle, star, and polka dot elements
- Each card type is automatically matched with a color scheme

See **references/design_guide.md** for detailed color palettes, ratio parameters, and JSON field descriptions.

## Screenshot Output

The generated HTML needs to be rendered as a PNG. Recommended methods:

1. **Playwright** (preferred): Use the playwright MCP tool, set the viewport to the width and height output by the script, then take a screenshot
2. **xbrowser skill**: Open the HTML and take a full-page screenshot
3. **browser tool**: If the HTML is accessible via HTTP, use the browser to take a screenshot

Once the screenshot is taken, the final PNG card image is ready and can be sent directly to the user.