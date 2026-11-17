---
name: product-icon-generator
description: "Icon Generator: Render a deterministic PNG icon, sprite, or texture at the requested width and height (1-4096 px). Use when an agent needs icon generator, product icon generator, create marketplace product icons, build minecraft and game sprite textures, design ui iconography at any size, render brand badges with transparent backgrounds, generate, idempotency key through AgentPMT-hosted remote tool calls. Discovery terms: icon generator, product icon generator, create marketplace product icons."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/product-icon-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/product-icon-generator"}}
---
# Icon Generator

## Freshness
Last updated: `2026-07-14`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Build crisp icons, sprites, and game-ready textures at any size from 1 to 4096 pixels. Compose them from rectangles, circles, lines, polygons, arcs, text, and transforms — and get a transparent or solid-background PNG ready to drop into apps, marketplaces, or game projects. A dedicated pixel-art mode produces hard-edged, integer-snapped output for 16×16, 32×32, and 64×64 sprites suitable for Minecraft mod textures, retro UI, deterministic favicons, and other small-format game assets. Every render is deterministic — the same inputs always produce the same PNG — and the returned file_id plugs directly into any downstream tool that accepts an image file_id.

## Product Instructions
### Icon Generator

Render deterministic PNG icons, sprites, textures, and small illustrations from
bounded drawing instructions. Generation creates one tenant-owned File Manager
record retained for 3 days.

#### Action: `generate`

Required:

- `idempotency_key`: UUID. Reuse it only for an exact retry.
- `instructions`: 1-256 drawing operations, including at least one drawable
  operation, with at most 8192 coordinate pairs across the request.

Optional:

- `width`, `height`: 1-4096 pixels, default 2048. Both are limited to 256 when
  `pixel_art_mode` is true.
- `pixel_art_mode`: disables anti-aliasing, snaps coordinates to integer pixels,
  and rejects text instructions.
- `continue_on_error`: records fixed, redacted renderer warnings and continues
  after a rendering failure only when at least one drawable operation succeeds.
  All skipped operations produce one aggregate operator warning. Structural
  validation errors always reject the request.
- `background_color`: `#RRGGBB`, `#RRGGBBAA`, `transparent`, or a documented
  named color; default `#FFFFFF`.

An idempotent retry returns the original `file_id` with a newly generated,
tenant-scoped signed URL. A reused UUID with a different payload is rejected. An
ambiguous storage outcome is never repeated automatically.

#### Drawing operations

Every instruction requires canonical `shape_type`. Unexpected fields are
rejected, including fields that belong to another shape.
Every drawable instruction must have paint whose effective alpha is non-zero;
`transparent`, `#RRGGBB00`, and `opacity: 0` are not usable drawing paint.

- `rectangle`: `x`, `y`, `width`, `height`; requires `fill` or `stroke`.
- `rounded_rectangle`: rectangle fields plus `radius`; requires paint.
- `circle`: center `x`, `y`, `radius`; requires paint.
- `ellipse`: center `x`, `y`, `radius_x`, `radius_y`; requires paint.
- `line`: at least two `points`; accepts `stroke`, `stroke_width`, `opacity`,
  and `anti_alias`.
- `polygon`: at least three `points`; requires `fill` or `stroke`.
- `arc`: center/radius plus `start_angle`, `end_angle`, and stroke fields.
- `text`: requires `text`; accepts `x`, `y`, `fill`, `font_size`,
  `font_family`, `font_weight` (`normal` or `bold`), and `text_align`. The font
  family must be installed on the renderer.
- `path`: requires an SVG path string and `fill` or `stroke`. Commands M, L, H,
  V, C, S, Q, T, A, and Z are supported.
- `save_state`, `restore_state`: bracket canvas state. Every save must have a
  matching restore and a restore cannot occur first.
- `translate`: requires `x` or `y`.
- `rotate`: requires `rotate`; optional `x` and `y` select its center.
- `scale`: requires non-zero `scale_x` or `scale_y` in the range -100 to 100.

Coordinates are limited to -16384 through 16384. Paths are capped at 100,000
characters and 8192 parsed segments; every parsed path coordinate uses the same
finite coordinate bound. Each line/polygon accepts at most 2048 distinct-capable
point pairs. Colors are strictly parsed. `opacity` is a 0-1 multiplier on the
original alpha channel. Pixel-art geometry that collapses after integer snapping
is rejected instead of producing a blank operation.

#### Examples

Smooth 256x256 icon:

```json
{"action":"generate","idempotency_key":"6ace54fe-f93d-4ba2-bfb8-98d4995120d8","width":256,"height":256,"background_color":"transparent","instructions":[{"shape_type":"circle","x":128,"y":128,"radius":100,"fill":"#2563EB"},{"shape_type":"path","path":"M78 130 L112 164 L180 88","stroke":"#FFFFFF","stroke_width":18}]}
```

16x16 pixel-art sprite:

```json
{"action":"generate","idempotency_key":"f7036c19-9013-42ea-8c88-6b0ff305455e","width":16,"height":16,"pixel_art_mode":true,"background_color":"transparent","instructions":[{"shape_type":"rectangle","x":7,"y":1,"width":2,"height":9,"fill":"#C0C0C0"},{"shape_type":"rectangle","x":5,"y":9,"width":6,"height":1,"fill":"#8B4513"},{"shape_type":"rectangle","x":7,"y":10,"width":2,"height":5,"fill":"#8B4513"}]}
```

#### Response and retention

The response includes `file_id`, `filename`, `signed_url`,
`signed_url_expires_in` (`15 minutes`), `size_bytes`, `expiration_date`,
`icon_details`, and `warnings`. The backing file expires after 3 days; the
signed URL is intentionally much shorter lived and is not persisted in the
idempotency record. An idempotent replay adds `idempotent_replay: true`.

Stable idempotency/storage failures include `IDEMPOTENCY_KEY_REUSED`,
`IDEMPOTENCY_IN_PROGRESS`, `IDEMPOTENCY_OUTCOME_UNKNOWN`, and
`IDEMPOTENCY_STORE_UNAVAILABLE`. Rendering/storage failures use
`ICON_RENDER_INSTRUCTION_INVALID`, `ICON_RENDER_FAILED`,
`ICON_STORAGE_UPLOAD_FAILED`, and `ICON_STORAGE_REPLAY_FAILED`. If the outcome
is unknown, inspect File Manager before deciding whether to submit a new UUID.

## When To Use
- Use this skill for `Icon Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: icon generator, product icon generator, create marketplace product icons, build minecraft and game sprite textures, design ui iconography at any size, render brand badges with transparent backgrounds, generate, idempotency key.
- Supported action names: `generate`.

## Use Cases
- Create marketplace product icons
- Build Minecraft and game sprite textures
- Design UI iconography at any size
- Render brand badges with transparent backgrounds
- Compose pixel-art assets deterministically
- Produce reference images for image-edit tools
- Generate consistent app icon sets at multiple sizes
- Render retro 16x16 and 32x32 sprite sheets
- Create transparent PNG favicons and small-format icons
- Generate Minecraft texture bindings for items
- blocks
- and entities

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `generate` (action slug: `generate`): Render a deterministic PNG and store it for 3 days. This creates one file; idempotent retries return the same file with a fresh 15-minute tenant-scoped signed URL. Price: `5` credits. Parameters: `background_color`, `continue_on_error`, `height`, `idempotency_key`, `instructions`, `pixel_art_mode`, `width`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "product-icon-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "product-icon-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "product-icon-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "product-icon-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "product-icon-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "product-icon-generator"
  }
}
```

## Call This Tool
Product slug: `product-icon-generator`

Marketplace page: https://www.agentpmt.com/marketplace/product-icon-generator

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Icon-Generator",
    "arguments": {
      "action": "generate",
      "background_color": "#FFFFFF",
      "continue_on_error": true,
      "height": 2048,
      "idempotency_key": "example idempotency key",
      "instructions": [
        {
          "anti_alias": true,
          "end_angle": -360000,
          "fill": "example fill",
          "font_family": "example font family",
          "font_size": 1,
          "font_weight": "normal",
          "height": 1,
          "opacity": 0
        }
      ],
      "pixel_art_mode": true,
      "width": 2048
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "product-icon-generator",
  "parameters": {
    "action": "generate",
    "background_color": "#FFFFFF",
    "continue_on_error": true,
    "height": 2048,
    "idempotency_key": "example idempotency key",
    "instructions": [
      {
        "anti_alias": true,
        "end_angle": -360000,
        "fill": "example fill",
        "font_family": "example font family",
        "font_size": 1,
        "font_weight": "normal",
        "height": 1,
        "opacity": 0
      }
    ],
    "pixel_art_mode": true,
    "width": 2048
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `generate` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/product-icon-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
