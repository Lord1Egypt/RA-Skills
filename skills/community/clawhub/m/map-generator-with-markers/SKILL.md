---
name: map-generator-with-markers
description: "Map Generator With Markers: Generate static maps with markers, paths, and labels. Multiple map types (roadmap, satellite, hybrid, terrain). Stored 7 days. Use when an agent needs map generator with markers, creating route maps with waypoints, generating location markers for reports, visualizing geographic data distributions, creating satellite view property maps, create map, points, map type through AgentPMT-hosted remote tool calls. Discovery terms: map generator with markers."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/map-generator-with-markers
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/map-generator-with-markers"}}
---
# Map Generator With Markers

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Generate custom static map with markers and optional paths connecting points. This tool creates map images with multiple markers that can be customized with colors, labels, and sizes, supports drawing paths between points with configurable colors and weights, offers multiple map types including roadmap, satellite, hybrid, and terrain views, allows precise zoom control and high DPI scaling for better image quality, and automatically stores generated images in cloud storage with 7-day expiration. Perfect for creating location-based visualizations, route maps, and geographic data presentations without requiring interactive map embedding.

## Product Instructions
### Map Generator With Markers

Generate static map images with custom markers and optional connecting paths between points.

#### Actions

##### create_map

Generate a static map image with one or more markers plotted at specific coordinates.

**Required Fields:**
- `points` (array): One or more point objects to plot. Each point requires:
  - `latitude` (number): Latitude coordinate (-90 to 90)
  - `longitude` (number): Longitude coordinate (-180 to 180)

**Optional Point Fields:**
- `label` (string): Single character A-Z or 0-9. Only displayed on default/mid size markers.
- `color` (string): Marker color name or hex code (e.g., `"red"`, `"blue"`, `"0xFFFF00"`)
- `size` (string): Marker size -- `"tiny"`, `"small"`, or `"mid"`

**Optional Map Fields:**
- `map_type` (string): `"roadmap"` (default), `"satellite"`, `"hybrid"`, or `"terrain"`
- `image_width` (integer): Width in pixels, max 640. Default: 640
- `image_height` (integer): Height in pixels, max 640. Default: 640
- `scale` (integer): 1 (default) or 2 for high-DPI/retina displays
- `zoom` (integer): Zoom level 0-21. Auto-calculated if omitted.
- `marker_color` (string): Default color for all markers (overridden by per-point color)
- `marker_size` (string): Default size for all markers (overridden by per-point size)
- `draw_path` (boolean): Set `true` to draw a line connecting points in order. Requires at least 2 points.
- `path_color` (string): Path line color in hex (e.g., `"0xFF0000"`). Default: `"0x0000ff"`
- `path_weight` (integer): Path line thickness in pixels, 1-20. Default: 5

**Example - Basic markers:**
```json
{
  "action": "create_map",
  "points": [
    {"latitude": 37.4220, "longitude": -122.0841, "label": "A"},
    {"latitude": 37.4275, "longitude": -122.1697, "label": "B"}
  ]
}
```

**Example - Styled markers with path on satellite view:**
```json
{
  "action": "create_map",
  "points": [
    {"latitude": 37.7749, "longitude": -122.4194, "label": "A", "color": "red"},
    {"latitude": 37.3382, "longitude": -121.8863, "label": "B", "color": "blue"}
  ],
  "draw_path": true,
  "path_color": "0xFF0000",
  "map_type": "hybrid"
}
```

**Example - Multiple locations with global marker styling:**
```json
{
  "action": "create_map",
  "points": [
    {"latitude": 40.7128, "longitude": -74.0060},
    {"latitude": 34.0522, "longitude": -118.2437},
    {"latitude": 41.8781, "longitude": -87.6298}
  ],
  "marker_color": "green",
  "marker_size": "mid",
  "map_type": "terrain",
  "image_width": 600,
  "image_height": 400
}
```

#### Response

The response includes:
- `signed_url` -- Link to the generated map image. Always present this to the user.
- `image_base64` -- Base64-encoded PNG for inline rendering
- `file_id` -- Storage identifier for the image
- `size_bytes` -- Image file size
- `points_count` -- Number of markers plotted
- `map_type`, `size`, `scale`, `zoom`, `draw_path` -- Confirms the settings used

#### Important Notes

- Use latitude/longitude coordinates for best reliability.
- Labels only display on default or mid-size markers. Tiny and small markers cannot show labels.
- When `draw_path` is enabled, at least 2 points are required.
- If zoom is omitted, the map auto-fits to show all markers.
- Maximum image dimensions are 640x640 pixels (before scale multiplier).
- Generated map images are available for 7 days via the signed URL.

## When To Use
- Use this skill for `Map Generator With Markers` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: map generator with markers, creating route maps with waypoints, generating location markers for reports, visualizing geographic data distributions, creating satellite view property maps, create map, points, map type.
- Supported action names: `create_map`.

## Use Cases
- Creating route maps with waypoints
- Generating location markers for reports
- Visualizing geographic data distributions
- Creating satellite view property maps
- Building delivery route visualizations
- Generating maps for presentations
- Creating location-based infographics
- Documenting field service locations
- Visualizing travel itineraries
- Creating real estate location maps

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `create_map` (action slug: `create-map`): Generate a static map image with markers plotted at specific coordinates, with optional path connecting points. Price: `20` credits. Parameters: `draw_path`, `image_height`, `image_width`, `map_type`, `marker_color`, `marker_size`, `path_color`, `path_weight`, plus 3 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "map-generator-with-markers"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "map-generator-with-markers"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "map-generator-with-markers"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "map-generator-with-markers"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "map-generator-with-markers"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "map-generator-with-markers"
  }
}
```

## Call This Tool
Product slug: `map-generator-with-markers`

Marketplace page: https://www.agentpmt.com/marketplace/map-generator-with-markers

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
    "name": "Map-Generator-With-Markers",
    "arguments": {
      "action": "create_map",
      "draw_path": false,
      "image_height": 640,
      "image_width": 640,
      "map_type": "roadmap",
      "marker_color": "example marker color",
      "marker_size": "tiny",
      "path_color": "0x0000ff",
      "path_weight": 5
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "map-generator-with-markers",
  "parameters": {
    "action": "create_map",
    "draw_path": false,
    "image_height": 640,
    "image_width": 640,
    "map_type": "roadmap",
    "marker_color": "example marker color",
    "marker_size": "tiny",
    "path_color": "0x0000ff",
    "path_weight": 5
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_map` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/map-generator-with-markers
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
