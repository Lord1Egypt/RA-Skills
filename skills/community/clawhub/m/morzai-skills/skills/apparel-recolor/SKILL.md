---
name: morzai-apparel-recolor
description: "Change garment colors from a target value or sample image, with part selection, logo or pattern handling, and 2K or 4K output."
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      remote_mcp_url: "https://recolor-api.lumo.me/mcp/v1/sse"
    auth: "oauth"
---

# AI Apparel Recolor

Professional AI garment recoloring suite for e-commerce.

## Core Capabilities
- **Part-Based Recolor**: Recolor specific garment parts such as upper body, coat, pants, hat, scarf, shoes, and bag.
- **Sample-Assisted Color Picking**: Use a reference image to extract a candidate color first, then apply the confirmed color to the target garment.
- **Explicit Pattern / Logo Handling**: Use a clear switch to keep existing logos/patterns, recolor them together, or remove them during recolor.
- **2K / 4K Output**: Supports standard and high-resolution output modes.

## Recommended Workflow
1. **User Intent Detection**: Parse natural language (e.g., "recolor only the coat", "keep the logo unchanged", "use the color from this sample").
2. **Color Confirmation**: If a sample image is provided, extract a candidate color first and confirm the selected target color before execution.
3. **Technical Mapping**: Reference [references/intent-mapping.md](references/intent-mapping.md) to choose part scope, logo/pattern behavior, and output mode.
4. **Execution**: Call the remote tool with a confirmed target color and the resolved garment parts.

## Knowledge Base
- [references/intent-mapping.md](references/intent-mapping.md) - Natural language to API parameter mapping logic.
- [references/recolor-palette.md](references/recolor-palette.md) - High-end fashion color presets.
- [references/fabric-texture-guide.md](references/fabric-texture-guide.md) - Current execution guardrails and unsupported assumptions.
