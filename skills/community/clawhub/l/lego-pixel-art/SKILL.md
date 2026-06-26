---
name: lego-pixel-art
description: Convert any image into LEGO brick pixel art, generating a complete building plan and material purchase list. Built-in standard LEGO color system, supports custom sizes (10-200 studs) and color precision adjustment, outputs a row-by-row building guide. Pure frontend implementation, zero dependencies, ready to use out of the box. Suitable for LEGO enthusiasts, craft creators, and educators.
---

# LEGO Pixel Art Generator

Convert any image into LEGO brick pixel art. Built-in 36 standard LEGO colors, supports custom stud dimensions and color precision, outputs a row-by-row building guide + material purchase list.

## Trigger Words
- LEGO pixel art
- lego pixel
- pixelate
- brick art

## Workflow

1. Confirm the user has an image (can provide a path/URL, or describe their needs)
2. Open the built-in tool `assets/pixel-lego.html`
3. Guide the user to drag the image into the tool, adjust parameters, and obtain the building plan

## Built-in Tool

Tool path: `assets/pixel-lego.html`

### Parameter Ranges

| Parameter | Range | Default |
|-----------|-------|---------|
| Width (studs) | 10–200 | 48 |
| Height (studs) | 10–200 | 48 |
| Color Precision | Levels 1–5 | 3 |

### Output Content

- Pixelated preview (with stud grid lines)
- Row-by-row building guide (lists required colors and quantities per row)
- Complete material list (color name + LEGO color code + required quantity)
- One-click copy list + export image

## Interaction Guide

When the user triggers this skill:

1. Inform the user that the tool is ready and display the tool page using a Hosted Embed
2. User uploads an image → Auto-pixelate and match LEGO colors
3. User can adjust width, height, and precision → Real-time preview
4. Switch to the "Building Guide" tab to view the row-by-row plan
5. Switch to the "Material List" tab to view the purchase list
6. Support exporting PNG images or copying text lists

If the user only describes the image content (without an actual image), ask if they would like to generate a sample image with corresponding colors.