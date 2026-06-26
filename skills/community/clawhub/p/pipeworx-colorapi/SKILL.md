---
name: pipeworx-colorapi
description: Color identification, scheme generation, and format conversion via TheColorAPI — hex, RGB, HSL, and CMYK
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🎨"
    homepage: https://pipeworx.io/packs/colorapi
---

# The Color API

Turn hex codes into rich color data. Identify a color's name, generate harmonious palettes, and convert between formats (hex, RGB, HSL, CMYK). Useful for design tools, accessibility checks, and brand color analysis.

## Tools

- **`identify_color`** — Pass a hex value (e.g., `"FF5733"`) to get the color's name, RGB/HSL/CMYK values, and contrast info
- **`generate_scheme`** — Create a color scheme from a seed color. Modes: monochrome, analogic, complement, triad, quad
- **`convert_color`** — Convert RGB values (0-255 per channel) to hex, HSL, CMYK, and get the nearest named color

## When to use

- A designer asks "what's the name of this hex color?"
- Generating a 5-color palette from a brand's primary color
- Converting between color formats for CSS, print, or design specs
- Checking if a color has good contrast for accessibility

## Example: generate a complementary palette from coral

```bash
curl -s -X POST https://gateway.pipeworx.io/colorapi/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"generate_scheme","arguments":{"hex":"FF6B6B","mode":"complement","count":5}}}'
```

Returns 5 colors with hex, RGB, HSL values and their closest named colors.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-colorapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/colorapi/mcp"]
    }
  }
}
```
