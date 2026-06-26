# Invoice Styles

InvoiceGen supports a few standard styles by modifying the CSS in the `invoice-template.html`. As an AI, you can adapt these styles on the fly based on the user's preference by tweaking the `{{BRAND_COLOR}}` and CSS properties.

## 1. Modern Clean (Default)
- **Font:** `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`
- **Brand Color:** `#0F172A` (Navy Slate)
- **Borders:** Thin, subtle `#eeeeee`
- **Layout:** Spaced out, airy, minimalist
- **Vibe:** Tech startup, agency, modern freelancer

## 2. Classic Professional
- **Font:** `Georgia, "Times New Roman", serif`
- **Brand Color:** `#1d4ed8` (Royal Blue) or `#000000` (Black)
- **Borders:** Thicker, more pronounced lines `#cccccc`
- **Table Headers:** Dark background with white text (`#333333` bg, `#ffffff` color)
- **Vibe:** Law firm, consulting group, traditional B2B

## 3. Minimal (No Borders)
- **Font:** `"Helvetica Neue", Helvetica, Arial, sans-serif`
- **Brand Color:** User's choice (often `#000000` or `#333333`)
- **Borders:** Only a single bottom border on the table header. No row borders.
- **Layout:** Extremely tight, relies on whitespace rather than lines.
- **Vibe:** High-end design studio, boutique agency

*Instructions for Agent:* If the user asks for a different style, modify the HTML template's CSS block before generating the PDF.