---
name: location-street-view-satellite-imagery
description: "Location Street View & Satellite Imagery: Get Street View panoramas, satellite/aerial imagery, and geocode. Use when an agent needs location street view & satellite imagery, location street view satellite imagery, real estate property visual verification and assessment, virtual site inspections for remote evaluation, travel itinerary generation with location previews, geographic data validation with visual confirmation, geocode, address through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery"}}
---
# Location Street View & Satellite Imagery

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Advanced location imagery and geocoding service that provides AI agents with comprehensive visual and geographic data capabilities. The tool seamlessly integrates Street View panoramic photography, satellite/aerial imagery, and bidirectional geocoding services into a unified interface. 

Core capabilities include retrieving 360-degree Street View images with precise camera control parameters (heading, pitch, field of view), capturing high-resolution satellite and hybrid map imagery at zoom levels from global to street-level detail, performing forward geocoding to convert addresses into precise geographic coordinates with place IDs and address components, and reverse geocoding to transform coordinates into structured addresses with locality information.

The tool automatically validates Street View availability before image retrieval, preventing failed requests and providing metadata including panorama IDs and capture dates. All generated images are stored securely for 7 days with both signed URLs for direct access and base64 encoding for inline data processing. The service handles multiple map types including roadmap, satellite, hybrid, and terrain views, supporting image dimensions up to 640x640 pixels.

Ideal for applications requiring visual location verification, the tool enables automated property assessment, travel planning with visual previews, geographic data validation, location-based content generation, and address verification workflows. The integrated storage system ensures efficient handling of imagery data while maintaining security through budget-scoped isolation.

## Product Instructions
### Location Street View & Satellite Imagery

Geocode addresses, reverse-geocode coordinates, and retrieve Street View and satellite/aerial images for any location worldwide.

---

#### Actions

##### geocode

Convert a street address or place name into geographic coordinates.

**Required fields:**
- `action` – `"geocode"`
- `address` (string) – Street address or place name to geocode

**Response includes:** formatted_address, location (lat/lng), place_id, address_components

**Example:**
```json
{
  "action": "geocode",
  "address": "1600 Amphitheatre Parkway, Mountain View, CA"
}
```

---

##### reverse_geocode

Convert latitude/longitude coordinates into a human-readable address.

**Required fields:**
- `action` – `"reverse_geocode"`
- `latitude` (number) – Latitude, -90 to 90
- `longitude` (number) – Longitude, -180 to 180

**Response includes:** formatted_address, place_id, address_components

**Example:**
```json
{
  "action": "reverse_geocode",
  "latitude": 37.4219999,
  "longitude": -122.0840575
}
```

---

##### get_street_view_image

Retrieve a Street View photograph for a location. Provide either an address or latitude/longitude coordinates.

**Required fields:**
- `action` – `"get_street_view_image"`
- `address` (string) **or** `latitude` + `longitude` (numbers) – The location to photograph

**Optional fields:**
- `heading` (integer, 0-360) – Camera compass heading in degrees. Omit to let the API choose automatically.
- `pitch` (integer, -90 to 90) – Camera vertical angle. Default: 0 (level). Negative values look down, positive look up.
- `fov` (integer, 1-120) – Field of view in degrees. Default: 90. Lower values zoom in.
- `image_width` (integer, max 640) – Image width in pixels. Default: 640.
- `image_height` (integer, max 640) – Image height in pixels. Default: 640.

**Response includes:** signed_url (image link to present to user), image_base64, file_id, size_bytes, pano_id, image_date, available (boolean)

**Example – by address with camera settings:**
```json
{
  "action": "get_street_view_image",
  "address": "1600 Amphitheatre Parkway, Mountain View, CA",
  "heading": 210,
  "pitch": 10
}
```

**Example – by coordinates:**
```json
{
  "action": "get_street_view_image",
  "latitude": 48.8584,
  "longitude": 2.2945,
  "heading": 0,
  "fov": 60
}
```

---

##### get_satellite_image

Retrieve a satellite, roadmap, hybrid, or terrain image for a location. Provide either an address or latitude/longitude coordinates.

**Required fields:**
- `action` – `"get_satellite_image"`
- `address` (string) **or** `latitude` + `longitude` (numbers) – The target location

**Optional fields:**
- `zoom` (integer, 0-21) – Zoom level. Default: 18. Higher values are more zoomed in (e.g., 15 = neighborhood, 18 = building-level, 21 = maximum detail).
- `map_type` (string) – One of `"satellite"`, `"roadmap"`, `"hybrid"`, `"terrain"`. Default: `"satellite"`.
- `image_width` (integer, max 640) – Image width in pixels. Default: 640.
- `image_height` (integer, max 640) – Image height in pixels. Default: 640.

**Response includes:** signed_url (image link to present to user), image_base64, file_id, size_bytes, zoom, map_type

**Example – satellite by coordinates:**
```json
{
  "action": "get_satellite_image",
  "latitude": 37.4219999,
  "longitude": -122.0840575,
  "zoom": 18,
  "map_type": "satellite"
}
```

**Example – hybrid map by address:**
```json
{
  "action": "get_satellite_image",
  "address": "Central Park, New York, NY",
  "zoom": 15,
  "map_type": "hybrid"
}
```

---

#### Common Workflows

1. **Address lookup then imagery** – Use `geocode` to get coordinates for an address, then pass those coordinates to `get_street_view_image` or `get_satellite_image`.
2. **Identify a location from coordinates** – Use `reverse_geocode` to find the address, then optionally get Street View imagery for context.
3. **Compare views** – Get both a Street View image (ground-level) and a satellite image (aerial) of the same location for a complete visual overview.

#### Important Notes

- **Image URLs:** Always present the `signed_url` from image responses to the user so they can view the image. URLs expire after 7 days.
- **Location input:** For image actions, provide either `address` or both `latitude` and `longitude` -- not both styles at once.
- **Street View availability:** Not all locations have Street View coverage. The response includes `available: false` when imagery is unavailable.
- **Image dimensions:** Maximum image size is 640x640 pixels.
- **Map types:** `satellite` shows raw aerial imagery, `hybrid` overlays road labels on satellite, `roadmap` shows a standard map, `terrain` shows elevation features.

## When To Use
- Use this skill for `Location Street View & Satellite Imagery` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: location street view & satellite imagery, location street view satellite imagery, real estate property visual verification and assessment, virtual site inspections for remote evaluation, travel itinerary generation with location previews, geographic data validation with visual confirmation, geocode, address.
- Supported action names: `geocode`, `get_satellite_image`, `get_street_view_image`, `reverse_geocode`.

## Use Cases
- Real estate property visual verification and assessment
- Virtual site inspections for remote evaluation
- Travel itinerary generation with location previews
- Geographic data validation with visual confirmation
- Automated report generation with embedded maps and street views
- Location-based decision support systems
- Field service documentation and verification
- Address validation and correction workflows
- Tourism and hospitality content creation
- Emergency response planning with visual context
- Urban planning and development analysis
- Insurance claim verification with imagery
- Logistics route planning with visual waypoints
- Environmental monitoring and change detection
- Educational geography and mapping applications

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `geocode` (action slug: `geocode`): Convert a street address or place name into geographic coordinates, place ID, and address components. Price: `15` credits. Parameters: `address`.
- `get_satellite_image` (action slug: `get-satellite-image`): Retrieve a satellite, roadmap, hybrid, or terrain image for a location. Returns a signed URL (valid 7 days), base64-encoded image, and metadata. Price: `15` credits. Parameters: `address`, `image_height`, `image_width`, `latitude`, `longitude`, `map_type`, `zoom`.
- `get_street_view_image` (action slug: `get-street-view-image`): Retrieve a Street View photograph for a location. Checks availability before fetching. Returns a signed URL (valid 7 days), base64-encoded image, and metadata including panorama ID and capture date. Price: `15` credits. Parameters: `address`, `fov`, `heading`, `image_height`, `image_width`, `latitude`, `longitude`, `pitch`.
- `reverse_geocode` (action slug: `reverse-geocode`): Convert latitude/longitude coordinates into a human-readable address with place ID and address components. Price: `15` credits. Parameters: `latitude`, `longitude`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "location-street-view-satellite-imagery"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "location-street-view-satellite-imagery"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "location-street-view-satellite-imagery"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "location-street-view-satellite-imagery"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "location-street-view-satellite-imagery"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "location-street-view-satellite-imagery"
  }
}
```

## Call This Tool
Product slug: `location-street-view-satellite-imagery`

Marketplace page: https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery

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
    "name": "Location-Street-View--Satellite-Imagery",
    "arguments": {
      "action": "geocode",
      "address": "example address"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "location-street-view-satellite-imagery",
  "parameters": {
    "action": "geocode",
    "address": "example address"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `geocode` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
