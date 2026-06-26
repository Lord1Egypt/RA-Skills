---
name: html_to_image
description: "Takes a URL, HTML file path, or raw HTML code and generates a printable image."
version: "1.0.0"
runtime: shell
entrypoint: "bash src/main.sh"

inputs:
  - name: source_type
    type: string
    description: "The type of source to render. Must be one of: 'url', 'file', 'code'."
    required: true
  - name: source_content
    type: string
    description: "The actual URL, absolute file path, or raw HTML string depending on source_type."
    required: true
  - name: format
    type: string
    description: "Output image format: 'png', 'jpeg', or 'webp'."
    required: false
    default: "png"
  - name: width
    type: integer
    description: "Viewport width in pixels."
    required: false
    default: 1200
  - name: full_page
    type: boolean
    description: "Whether to capture the full scrollable page."
    required: false
    default: false

output:
  type: json
  description: "JSON object containing the absolute path to the generated image file and its metadata."
---

# HTML to Image Skill (via agent-browser)

This skill utilizes OpenClaw's `agent-browser` composition to render a URL, local HTML file, or raw HTML string into an image. It executes a lightweight Bash script wrapper.

## Usage Guide
When using this skill to generate an image, provide the `source_type` and `source_content`.

- **source_type**: The content format (`url`, `file`, or `code`).
- **source_content**: The target URL, absolute file path, or HTML code block.
- **format**: The desired image format (`png`, `jpeg`, or `webp`). Default is `png`.
- **width**: The width of the browser viewport. Default is 1200px.
- **full_page**: Set to `true` to take a full page screenshot instead of just the viewport.
