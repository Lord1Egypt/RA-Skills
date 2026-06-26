---
name: morzai-clothing-adjustment
description: "Apply preset-based whole-garment cleanup for wrinkles, lint, pet hair, and a cleaner flatter presentation."
metadata:
  openclaw:
    emoji: "👔"
    requires:
      remote_mcp_url: "https://adjustment-api.lumo.me/mcp/v1/sse"
---

# AI Clothing Adjustment

Preset-driven garment cleanup suite for fashion imagery.

## Core Capabilities
- **Whole-Garment Cleanup**: Improve the overall clothing look using a single approved preset.
- **Wrinkle Reduction**: Support light, balanced, or strong wrinkle-cleanup intent at the preset level.
- **Surface Cleanup**: Support overall cleanup requests such as lint, dust, pet hair, and minor blemish removal when covered by the chosen preset.
- **Preview-First Workflow**: Best suited for previewing and exporting one overall clothing-adjustment result.

## Recommended Workflow
1. **Intent Compression**: Collapse the user's request into one overall goal such as light cleanup, balanced cleanup, strong flattening, or surface cleanup.
2. **Preset Selection**: Use [references/intent-mapping.md](references/intent-mapping.md) to choose one approved preset direction.
3. **Expectation Setting**: If the user asks for per-part masking or independent sliders, explain that current support is preset-level whole-image adjustment only.
4. **Execution**: Run one whole-garment adjustment preset instead of assembling multiple fine-grained controls.

## Knowledge Base
- [references/intent-mapping.md](references/intent-mapping.md) - Natural language to preset-selection mapping.
