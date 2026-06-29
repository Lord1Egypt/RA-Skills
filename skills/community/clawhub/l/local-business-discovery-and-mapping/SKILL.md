---
name: local-business-discovery-and-mapping
description: "Local Business Discovery and Mapping: Search for nearby places or by text query. 30+ category filters. Use when an agent needs local business discovery and mapping, local business discovery and recommendations for travel planning, restaurant and dining venue search for meal planning applications, healthcare facility location for medical service directories, retail store finding for shopping assistance, geocode, address, nearby search through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping"}}
---
# Local Business Discovery and Mapping

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Comprehensive place discovery and geocoding service that enables AI agents to search, discover, and analyze physical locations in the real world. The tool provides powerful search capabilities with two primary modes: nearby search for radius-based discovery and text search for flexible keyword-based queries across global locations.

The nearby search functionality supports advanced filtering through 30+ predefined category groups, intelligently organized into logical clusters such as restaurants_and_dining (covering 37 restaurant types from fast food to fine dining), health_and_medical (hospitals, doctors, pharmacies), entertainment_and_attractions (museums, theaters, amusement parks), and transportation (airports, train stations, transit stops). Each category group automatically expands to include all relevant place types, enabling precise filtering without manual specification of individual types.

Core capabilities include discovering places within a 1-50km radius of any location, searching globally with text queries and optional location bias, forward geocoding to convert addresses into coordinates with place IDs and address components, reverse geocoding to transform coordinates into structured addresses, and intelligent category-based filtering with both inclusion and exclusion options. The tool returns rich place data including names, addresses, ratings, price levels, operating status, and precise coordinates.

The tool automatically handles address-to-coordinate conversion when needed, allowing agents to specify search centers using either street addresses or lat/lng coordinates. All searches support configurable result limits up to 50 places per query, with detailed metadata for each discovered location. The integrated geocoding ensures seamless workflow between address-based and coordinate-based operations.

## Product Instructions
### Local Business Discovery and Mapping

Search for nearby businesses, find places by text query, and convert between addresses and coordinates using Google Maps.

#### Actions

##### nearby_search

Search for places near a location by category.

**Required:** At least one of `address` OR (`latitude` + `longitude`)

**Optional:**
- `included_types` (array) - Category groups to include (see Category Groups below)
- `excluded_types` (array) - Category groups to exclude
- `radius_meters` (integer, 1-50000, default: 1000) - Search radius in meters
- `max_results` (integer, 1-50, default: 50) - Maximum results to return

**Example - Find restaurants near an address:**
```json
{
  "action": "nearby_search",
  "address": "Times Square, New York, NY",
  "included_types": ["restaurants_and_dining"],
  "radius_meters": 500,
  "max_results": 10
}
```

**Example - Find hotels near coordinates:**
```json
{
  "action": "nearby_search",
  "latitude": 40.7580,
  "longitude": -73.9855,
  "included_types": ["lodging_and_accommodation"],
  "radius_meters": 2000
}
```

**Example - Find everything except restaurants:**
```json
{
  "action": "nearby_search",
  "address": "Downtown Chicago, IL",
  "excluded_types": ["restaurants_and_dining", "cafes_and_light_fare"],
  "radius_meters": 1000
}
```

---

##### text_search

Search for places using a free-text query. Optionally bias results toward a location.

**Required:**
- `query` (string) - The search text

**Optional:**
- `address` (string) - Bias results toward this address
- `latitude` / `longitude` (number) - Bias results toward these coordinates
- `radius_meters` (integer, 1-50000, default: 1000) - Bias radius in meters
- `max_results` (integer, 1-50, default: 50) - Maximum results to return

**Example - Search by query with location bias:**
```json
{
  "action": "text_search",
  "query": "best pizza in Brooklyn",
  "address": "Brooklyn, NY",
  "radius_meters": 5000,
  "max_results": 10
}
```

**Example - Search without location bias:**
```json
{
  "action": "text_search",
  "query": "Statue of Liberty"
}
```

---

##### geocode

Convert a street address or place name into geographic coordinates.

**Required:**
- `address` (string) - The address or place name to geocode

**Example:**
```json
{
  "action": "geocode",
  "address": "1600 Amphitheatre Parkway, Mountain View, CA"
}
```

**Returns:** Formatted address, latitude/longitude, place ID, and address components.

---

##### reverse_geocode

Convert geographic coordinates into a human-readable address.

**Required:**
- `latitude` (number, -90 to 90)
- `longitude` (number, -180 to 180)

**Example:**
```json
{
  "action": "reverse_geocode",
  "latitude": 37.4224764,
  "longitude": -122.0842499
}
```

**Returns:** Formatted address, place ID, and address components.

---

#### Category Groups

Use these values in `included_types` and `excluded_types` for `nearby_search`:

| Category | What It Includes |
|---|---|
| restaurants_and_dining | Restaurants of all cuisines (Italian, Chinese, Mexican, etc.), fast food, fine dining, steakhouses |
| cafes_and_light_fare | Coffee shops, tea houses, cafes, bagel/donut/juice shops |
| bars_and_nightlife | Bars, pubs, wine bars, night clubs, karaoke |
| bakeries_and_sweets | Bakeries, candy stores, ice cream shops, chocolate shops |
| food_retail_and_markets | Grocery stores, supermarkets, delis, butcher shops, convenience stores |
| food_services | Catering, food courts, food delivery, sandwich shops |
| lodging_and_accommodation | Hotels, motels, hostels, B&Bs, resorts, inns |
| shopping_general | Malls, department stores, discount stores, gift shops |
| shopping_specialty_retail | Book stores, clothing, jewelry, electronics, pet stores, florists |
| automotive | Car dealers, repair, rental, car wash, gas stations, EV charging |
| health_and_medical | Hospitals, doctors, dentists, chiropractors, pharmacies |
| beauty_and_personal_care | Salons, barber shops, spas, nail salons, wellness centers |
| fitness_and_sports | Gyms, sports clubs, swimming pools, yoga studios, bowling alleys |
| parks_and_nature | Parks, gardens, beaches, hiking areas, wildlife parks |
| entertainment_and_attractions | Amusement parks, zoos, aquariums, movie theaters, casinos |
| arts_and_culture | Museums, art galleries, cultural centers, historical landmarks |
| performing_arts_and_venues | Theaters, concert halls, arenas, stadiums, event venues |
| religious_sites | Churches, mosques, synagogues, temples |
| education | Schools, universities, preschools, camps |
| government_and_civic | City hall, courthouses, post offices, police/fire stations |
| financial_services | Banks, ATMs, accounting firms, insurance agencies |
| professional_services | Lawyers, consultants, real estate agencies |
| home_services_and_contractors | Electricians, plumbers, locksmiths, hardware stores, moving companies |
| transportation | Airports, train stations, bus stops, subway stations, ferry terminals |
| travel_and_tourism | Travel agencies, tour operators, visitor centers |
| residential | Apartment buildings, condos, housing complexes |
| geographic_administrative | Countries, states, cities, postal codes |
| outdoor_recreation | Campgrounds, RV parks, farms, ski resorts |
| community_and_social | Community centers, libraries, public baths |
| miscellaneous_services | Laundry, tailors, courier services, veterinary care |

#### Common Workflows

**Find and locate a business type:**
1. Use `nearby_search` with a category to find businesses near a location
2. Use `geocode` to get exact coordinates for any address from the results

**Identify what is at a location:**
1. Use `reverse_geocode` with coordinates to get the address
2. Use `nearby_search` with those coordinates to discover surrounding businesses

**Search and filter:**
1. Use `text_search` with a descriptive query for broad results
2. Use `nearby_search` with `included_types` for category-specific filtered results

#### Important Notes

- For `nearby_search`, you must provide either an `address` or both `latitude` and `longitude`. If you provide an address, it is automatically geocoded to coordinates.
- For `text_search`, location parameters are optional and serve as a bias (not a strict boundary).
- The `included_types` and `excluded_types` parameters only apply to `nearby_search`. They do not work with `text_search`.
- Maximum search radius is 50,000 meters (50 km).
- Maximum results per request is 50.

## When To Use
- Use this skill for `Local Business Discovery and Mapping` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: local business discovery and mapping, local business discovery and recommendations for travel planning, restaurant and dining venue search for meal planning applications, healthcare facility location for medical service directories, retail store finding for shopping assistance, geocode, address, nearby search.
- Supported action names: `geocode`, `nearby_search`, `reverse_geocode`, `text_search`.

## Use Cases
- Local business discovery and recommendations for travel planning
- Restaurant and dining venue search for meal planning applications
- Healthcare facility location for medical service directories
- Retail store finding for shopping assistance
- Hotel and accommodation search for booking systems
- Emergency service location finding for safety applications
- Transportation hub discovery for route planning
- Educational institution search for school finders
- Entertainment venue discovery for event planning
- Park and recreation area finding for outdoor activities
- Professional service provider location for business directories
- Real estate area analysis with nearby amenities
- Market research for competitor analysis and site selection
- Delivery service area validation and address verification
- Tourism point of interest discovery for travel guides

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `geocode` (action slug: `geocode`): Convert a street address or place name into geographic coordinates, place ID, and address components. Price: `20` credits. Parameters: `address`.
- `nearby_search` (action slug: `nearby-search`): Search for places near a location by category. Requires either an address or latitude/longitude coordinates. Automatically geocodes addresses to coordinates. Price: `20` credits. Parameters: `address`, `excluded_types`, `included_types`, `latitude`, `longitude`, `max_results`, `radius_meters`.
- `reverse_geocode` (action slug: `reverse-geocode`): Convert latitude/longitude coordinates into a human-readable address with place ID and address components. Price: `20` credits. Parameters: `latitude`, `longitude`.
- `text_search` (action slug: `text-search`): Search for places using a free-text query. Optionally bias results toward a specific location. Price: `20` credits. Parameters: `address`, `latitude`, `longitude`, `max_results`, `query`, `radius_meters`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "local-business-discovery-and-mapping"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "local-business-discovery-and-mapping"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "local-business-discovery-and-mapping"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "local-business-discovery-and-mapping"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "local-business-discovery-and-mapping"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "local-business-discovery-and-mapping"
  }
}
```

## Call This Tool
Product slug: `local-business-discovery-and-mapping`

Marketplace page: https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping

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
    "name": "Local-Business-Discovery-and-Mapping",
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
  "name": "local-business-discovery-and-mapping",
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
- Marketplace product: https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
