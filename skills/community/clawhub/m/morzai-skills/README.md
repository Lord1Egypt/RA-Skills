# Morzai AI E-commerce Skills (Master Suite)

A professional collection of AI-powered image processing skills for e-commerce, organized into a router plus two capability layers.

Designed for global sellers on platforms like Amazon, Shopify, Temu, and SHEIN.

## Root Skill Design

The root [`SKILL.md`](SKILL.md) remains a thin router.

- It reads [`api/commands.json`](api/commands.json) as the single source of truth for routing, required inputs, and execution mapping.
- It asks only for missing required inputs.
- It then opens the routed child skill and continues execution in the same user-facing agent.
- It does not duplicate child-skill capability details at the root layer.

## Architecture

### Layer 1: Single-Function Editing
Focuses on one editing job at a time.

| Skill | Description |
|-------|-------------|
| [apparel-recolor](skills/apparel-recolor) | Garment recolor workflow. |
| [garment-retouch](skills/garment-retouch) | Apparel cleanup workflow. |
| [clothing-adjustment](skills/clothing-adjustment) | Preset-based garment cleanup workflow. |

### Layer 2: Composite Listing Workflow
Focuses on multi-image ecommerce deliverables.

| Skill | Description |
|-------|-------------|
| [morzai-ecommerce-product-kit](skills/ecommerce-product-kit) | Ecommerce image kit workflow. |

## Notes

- Routing stays at the root layer; task details stay in child skills.
- Child skills declare their own execution boundary.
- User-facing output should stay minimal and operational.

## Requirements

- **MORZAI_API_KEY**: Optional credential override for CLI-based workflows.
- **Morzai CLI**: `morzai-ecommerce-product-kit` now expects the public `morzai` CLI to be installed and configured.
- **Claude Code CLI**: Or any skills-compatible AI agent (Cursor, Codex, etc.).

## License

MIT
