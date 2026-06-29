---
name: multi-location-route-optimizer-w-map
description: "Multi-Location Route Optimizer W Map: Optimize routes for 2-25 waypoints. Use when an agent needs multi location route optimizer w map, delivery services can optimize daily delivery routes to save fuel and time while handling up to 25 deliveries per route with automatic distance and time calculations. sales teams can plan efficient customer visit schedules and prioritize high value clients while minimizing travel between appointments. Discovery terms: multi location route optimizer w map."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map"}}
---
# Multi-Location Route Optimizer W Map

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Find the most efficient route for visiting multiple locations with this comprehensive route optimization tool. Perfect for delivery services, sales teams, service technicians, and any business that needs to minimize travel time or distance when visiting multiple locations. The tool automatically reorders 2-25 waypoints to find the most efficient path, accepting both street addresses and latitude/longitude coordinates for maximum flexibility. It generates static maps showing the optimized route and creates shareable Google Maps URLs for easy navigation. The optimizer supports round trips for delivery scenarios, accounts for service time at each location, and offers multiple travel modes including driving, walking, bicycling, and transit. You can avoid tolls, highways, or ferries based on your preferences, and choose to optimize for either time or distance. The tool provides four main actions: optimize_route to find the most efficient order to visit all locations, get_route_details for turn-by-turn directions, create_route_map to generate visual maps, and get_instructions for usage documentation. Typical users see 10-30% reduction in travel distance and time, making this an essential tool for improving operational efficiency.

## Product Instructions
### Multi-Location Route Optimizer W Map

Optimizes multi-stop routes to find the most efficient visit order, provides turn-by-turn directions, and generates visual route maps. Supports 2-25 locations with driving, walking, bicycling, and transit modes.

#### Actions

##### optimize_route

Finds the most efficient order to visit a set of locations, minimizing total travel time or distance.

**Required fields:**
- `locations` (array): 2-25 location objects. Each must have either `address` (string) OR `latitude`/`longitude` (numbers).

**Optional location fields:**
- `name` (string): Label for the location (e.g., "Warehouse", "Customer A")
- `service_time_minutes` (integer): Time spent at this stop in minutes

**Optional fields:**
- `start_location` (object): Fixed starting point if different from first location. Object with `address` or `latitude`/`longitude`, and optional `name`.
- `end_location` (object): Fixed ending point if different from last location. Object with `address` or `latitude`/`longitude`, and optional `name`. Ignored when `return_to_start` is true.
- `return_to_start` (boolean): Set to `true` for a round trip back to starting location. Default: `false`
- `travel_mode` (string): `"driving"` (default), `"walking"`, `"bicycling"`, or `"transit"`
- `optimize_for` (string): `"time"` (default) or `"distance"`
- `avoid` (array): Features to avoid: `"tolls"`, `"highways"`, `"ferries"`
- `departure_time` (string): ISO format datetime (e.g., `"2026-01-15T09:00:00"`) or `"now"`. Traffic-aware routing (driving mode only).
- `include_map` (boolean): Generate a visual route map image. Default: `false`
- `include_directions` (boolean): Include turn-by-turn directions. Default: `false`
- `map_width` (integer): Map image width in pixels, 1-640. Default: 640
- `map_height` (integer): Map image height in pixels, 1-640. Default: 640

**Response includes:**
- `optimized_route.locations` - Locations in optimized order with `travel_to_next_km` and `travel_to_next_minutes` per stop
- `optimized_route.legs` - Per-leg breakdown with `from`, `to`, `distance_km`, `duration_minutes`
- `optimized_route.total_distance_km` - Total route distance
- `optimized_route.total_duration_minutes` - Total travel time plus service time
- `optimized_route.estimated_fuel_cost_usd` - Rough fuel cost estimate
- `google_maps_url` - Clickable Google Maps navigation link
- `optimization_stats` - Distance/time saved compared to original order
- `map_image.signed_url` - Route map image URL (when `include_map: true`). Always present this URL to the user.
- `directions` - Turn-by-turn directions (when `include_directions: true`)

**Example - Basic optimization:**
```json
{
  "action": "optimize_route",
  "locations": [
    { "address": "San Francisco, CA" },
    { "address": "San Jose, CA" },
    { "address": "Oakland, CA" }
  ]
}
```

**Example - Full-featured delivery route:**
```json
{
  "action": "optimize_route",
  "locations": [
    { "address": "123 Main St, San Francisco, CA", "name": "Warehouse", "service_time_minutes": 15 },
    { "address": "456 Oak Ave, San Jose, CA", "name": "Customer A", "service_time_minutes": 30 },
    { "address": "789 Pine St, Oakland, CA", "name": "Customer B", "service_time_minutes": 20 }
  ],
  "start_location": { "address": "100 HQ Blvd, San Francisco, CA", "name": "HQ" },
  "return_to_start": true,
  "travel_mode": "driving",
  "optimize_for": "time",
  "avoid": ["tolls"],
  "include_map": true,
  "include_directions": true
}
```

**Example - Using coordinates:**
```json
{
  "action": "optimize_route",
  "locations": [
    { "latitude": 37.7749, "longitude": -122.4194, "name": "San Francisco" },
    { "latitude": 37.3382, "longitude": -121.8863, "name": "San Jose" },
    { "latitude": 37.8044, "longitude": -122.2712, "name": "Oakland" }
  ]
}
```

---

##### get_route_details

Gets turn-by-turn directions for locations in the order provided (does not reorder them).

**Required fields:**
- `locations` (array): 2-25 location objects in the desired visit order

**Optional fields:**
- `travel_mode` (string): `"driving"` (default), `"walking"`, `"bicycling"`, or `"transit"`
- `avoid` (array): Features to avoid: `"tolls"`, `"highways"`, `"ferries"`

**Response includes:**
- `directions.legs[]` - Per-leg directions with steps, distance, and duration
- `directions.total_distance` - Total distance in km
- `directions.total_duration` - Total duration in minutes
- `google_maps_url` - Clickable Google Maps link

**Example:**
```json
{
  "action": "get_route_details",
  "locations": [
    { "address": "Times Square, New York, NY", "name": "Start" },
    { "address": "Central Park, New York, NY", "name": "Stop 1" },
    { "address": "Brooklyn Bridge, New York, NY", "name": "End" }
  ],
  "travel_mode": "walking"
}
```

---

##### create_route_map

Generates a static map image showing the route with labeled markers at each location.

**Required fields:**
- `locations` (array): 2-25 location objects in the desired order

**Optional fields:**
- `travel_mode` (string): `"driving"` (default), `"walking"`, `"bicycling"`, or `"transit"`
- `map_width` (integer): Image width in pixels, 1-640. Default: 640
- `map_height` (integer): Image height in pixels, 1-640. Default: 640

**Response includes:**
- `map_image.signed_url` - URL to the generated map image. Always present this URL to the user.
- `map_image.file_id` - Storage file ID
- `google_maps_url` - Clickable Google Maps link

**Example:**
```json
{
  "action": "create_route_map",
  "locations": [
    { "address": "Los Angeles, CA", "name": "LA" },
    { "address": "Las Vegas, NV", "name": "Vegas" },
    { "address": "Phoenix, AZ", "name": "Phoenix" }
  ],
  "map_width": 640,
  "map_height": 400
}
```

#### Important Notes

- Each location must have either an `address` OR both `latitude` and `longitude`.
- You can mix address-based and coordinate-based locations in the same request.
- The `locations` array must contain between 2 and 25 locations.
- When `return_to_start` is `true`, the route ends back at the starting point; `end_location` is ignored.
- Map images expire after 7 days. Always display the `signed_url` to the user when a map is generated.
- The `google_maps_url` in every response opens the route in Google Maps for interactive navigation.
- Optimization uses a nearest-neighbor algorithm; results are very good for typical route sizes but may not be globally optimal for very large sets.
- Set `departure_time` to `"now"` or an ISO datetime to factor in traffic conditions (driving mode only).

## When To Use
- Use this skill for `Multi-Location Route Optimizer W Map` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: multi location route optimizer w map, delivery services can optimize daily delivery routes to save fuel and time while handling up to 25 deliveries per route with automatic distance and time calculations. sales teams can plan efficient customer visit schedules and prioritize high value clients while minimizing travel between appointments. service technicians can reduce travel time between service calls and include service duration at each stop for accurate scheduling. real estate agents can organize property showings efficiently and create optimal routes for touring multiple properties with clients. food trucks and mobile businesses can plan optimal stop locations throughout the day to maximize coverage while minimizing fuel costs. tour operators can create efficient sightseeing routes that balance tourist attractions with practical travel considerations., create route map, locations, travel mode, map width, map height, get route details.
- Supported action names: `create_route_map`, `get_route_details`, `optimize_route`.

## Use Cases
- Delivery services can optimize daily delivery routes to save fuel and time while handling up to 25 deliveries per route with automatic distance and time calculations. Sales teams can plan efficient customer visit schedules and prioritize high-value clients while minimizing travel between appointments. Service technicians can reduce travel time between service calls and include service duration at each stop for accurate scheduling. Real estate agents can organize property showings efficiently and create optimal routes for touring multiple properties with clients. Food trucks and mobile businesses can plan optimal stop locations throughout the day to maximize coverage while minimizing fuel costs. Tour operators can create efficient sightseeing routes that balance tourist attractions with practical travel considerations.

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `create_route_map` (action slug: `create-route-map`): Generate a static map image showing the route with labeled markers at each location. Price: `25` credits. Parameters: `locations`, `map_height`, `map_width`, `travel_mode`.
- `get_route_details` (action slug: `get-route-details`): Get turn-by-turn directions for locations in the provided order (does not reorder them). Price: `25` credits. Parameters: `avoid`, `locations`, `travel_mode`.
- `optimize_route` (action slug: `optimize-route`): Find the most efficient order to visit 2-25 locations, minimizing total travel time or distance. Returns optimized route with distance/duration totals, a Google Maps navigation URL, and optimization stats. Price: `25` credits. Parameters: `avoid`, `departure_time`, `end_location`, `include_directions`, `include_map`, `locations`, `map_height`, `map_width`, plus 4 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "multi-location-route-optimizer-w-map"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "multi-location-route-optimizer-w-map"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "multi-location-route-optimizer-w-map"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "multi-location-route-optimizer-w-map"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "multi-location-route-optimizer-w-map"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "multi-location-route-optimizer-w-map"
  }
}
```

## Call This Tool
Product slug: `multi-location-route-optimizer-w-map`

Marketplace page: https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map

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
    "name": "Multi-Location-Route-Optimizer-W-Map",
    "arguments": {
      "action": "create_route_map",
      "locations": [
        {
          "address": "example address",
          "latitude": -90,
          "longitude": -180,
          "name": "example name",
          "service_time_minutes": 0
        }
      ],
      "map_height": 640,
      "map_width": 640,
      "travel_mode": "driving"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "multi-location-route-optimizer-w-map",
  "parameters": {
    "action": "create_route_map",
    "locations": [
      {
        "address": "example address",
        "latitude": -90,
        "longitude": -180,
        "name": "example name",
        "service_time_minutes": 0
      }
    ],
    "map_height": 640,
    "map_width": 640,
    "travel_mode": "driving"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_route_map` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
