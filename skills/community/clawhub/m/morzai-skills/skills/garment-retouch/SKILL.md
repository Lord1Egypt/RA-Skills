---
name: morzai-garment-retouch
description: "Retouch apparel images for ghost mannequin removal, hanger cleanup, and cleaner product outputs with simple intensity and resolution controls."
metadata:
  openclaw:
    emoji: "👕"
    requires:
      remote_mcp_url: "https://retouch-api.lumo.me/mcp/v1/sse"
---

# AI Garment Retouch

Advanced AI retouching for ghost mannequin effects and apparel-specific background cleanup.

## Core Capabilities
- **Ghost Mannequin Removal**: Automatically in-fill internal neckline and sleeve details occupied by mannequins.
- **Background Cleanup**: Erase hangers, background debris, and unwanted shadows for e-commerce.
- **V2 Enhanced Model**: 4K resolution and high-intensity reconstruction for complex occlusions.

## Recommended Workflow
1. **Model Selection**: Default to `model_version: "v2.0"` for the best performance and 4K support.
2. **Intent Mapping**: Use [references/intent-mapping.md](references/intent-mapping.md) to set `correction_intensity` (low to high).

## Knowledge Base
- [references/intent-mapping.md](references/intent-mapping.md) - Goal-to-API mapping for retouching.
- [references/ghost-mannequin-specs.md](references/ghost-mannequin-specs.md) - Professional specs for neck/sleeve in-filling.
- [references/output-resolutions.md](references/output-resolutions.md) - Resolution requirements for Amazon/Shopify.
