---
name: google-maps-places
description: Google Maps and Places API integration. Search places, geocode addresses, calculate routes, get directions, and retrieve location data. Use this skill when users want to look up locations, convert addresses to coordinates, or get routing information.
---

# Google Maps

![Google Maps](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-maps.svg?v=2)

Access Google Maps and Places API via ClawLink managed credentials. Search places, geocode addresses, calculate routes, get directions, and retrieve location data.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-maps-places) for hosted connection flows and credentials so you do not need to configure Google Maps API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Maps |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Maps |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Maps   │
│   (User Chat)   │     │   (OAuth)    │     │  (Places/Routes) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Maps      │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Maps    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Maps again."

## Quick Start

```bash
# Search for places
clawlink_call_tool --tool "googlemaps_search_places" --params '{"query": "coffee shop nearby"}'

# Geocode an address
clawlink_call_tool --tool "googlemaps_geocode" --params '{"address": "1600 Amphitheatre Parkway, Mountain View, CA"}'

# Get directions
clawlink_call_tool --tool "googlemaps_directions" --params '{"origin": "San Francisco, CA", "destination": "Los Angeles, CA"}'
```

## Authentication

All Google Maps tool calls are authenticated automatically by ClawLink using the user's connected Google account or API key.

**No API key is required in chat.** ClawLink handles credential management and injects it into every Google Maps API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-maps and connect Google Maps.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-maps` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-maps
```

**Response:** Returns the live tool catalog for Google Maps.

### Reconnect

If Google Maps tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-maps
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-maps`

## Security & Permissions

- Access is scoped to location and routing data available through the Google Maps API.
- **Write operations require explicit user confirmation.** Before executing any call that modifies data, confirm the target and intended effect with the user.
- Geocoding and routing are read-only operations that do not modify any data.

## Tool Reference

### Place Search & Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_search_places` | Search for places by text query, category, or name | Read |
| `googlemaps_nearby_search` | Find places near a location within a radius | Read |
| `googlemaps_place_details` | Get detailed information about a specific place | Read |
| `googlemaps_find_place` | Find a place from a text query or phone number | Read |
| `googlemaps_autocomplete` | Get place suggestions as the user types | Read |

### Geocoding & Address Lookup

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_geocode` | Convert an address to latitude/longitude coordinates | Read |
| `googlemaps_reverse_geocode` | Convert coordinates back to a human-readable address | Read |

### Routing & Directions

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_directions` | Get directions between origin and destination with multiple modes | Read |
| `googlemaps_distance_matrix` | Calculate distances and travel times between multiple origins and destinations | Read |
| `googlemaps_route_matrix` | Get route information for multiple origin-destination pairs | Read |

### Elevation & Terrain

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_elevation` | Get elevation data for locations on the earth | Read |
| `googlemaps_elevation_along_path` | Get elevation data along a path | Read |

### Time Zone

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_timezone` | Get the time zone for a location | Read |

### Roads

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_snap_to_roads` | Snap GPS points to the nearest road segments | Read |
| `googlemaps_nearest_roads` | Get the nearest road segments to given coordinates | Read |

### Geolocation

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_geolocate` | Get a device's location from cell towers and WiFi nodes | Read |

### Static Maps

| Tool | Description | Mode |
|------|-------------|------|
| `googlemaps_static_maps` | Generate a static map image with markers and paths | Read |

## Code Examples

### Search for a place

```bash
clawlink_call_tool --tool "googlemaps_search_places" \
  --params '{
    "query": "Italian restaurant",
    "location": {"latitude": 37.7749, "longitude": -122.4194},
    "radius": 1000
  }'
```

### Geocode an address

```bash
clawlink_call_tool --tool "googlemaps_geocode" \
  --params '{
    "address": "1 Apple Park Way, Cupertino, CA 95014"
  }'
```

### Get directions

```bash
clawlink_call_tool --tool "googlemaps_directions" \
  --params '{
    "origin": "San Francisco, CA",
    "destination": "Yosemite National Park, CA",
    "mode": "driving",
    "waypoints": [{"stop_over": true, "location": "Palo Alto, CA"}]
  }'
```

### Get distance matrix

```bash
clawlink_call_tool --tool "googlemaps_distance_matrix" \
  --params '{
    "origins": ["San Francisco, CA", "Oakland, CA"],
    "destinations": ["Los Angeles, CA", "San Diego, CA"],
    "mode": "driving"
  }'
```

### Get place details

```bash
clawlink_call_tool --tool "googlemaps_place_details" \
  --params '{
    "place_id": "YOUR_PLACE_ID",
    "fields": ["name", "formatted_address", "rating", "reviews", "opening_hours"]
  }'
```

### Reverse geocode

```bash
clawlink_call_tool --tool "googlemaps_reverse_geocode" \
  --params '{
    "location": {"latitude": 37.4220, "longitude": -122.0841}
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Maps is connected.
2. Call `clawlink_list_tools --integration google-maps` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-maps`.
5. If no Google Maps tools appear, direct the user to https://claw-link.dev/dashboard?add=google-maps.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  search → get → geocode → directions → call                 │
│                                                             │
│  Example: Search places → Get details → Show results       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE / HIGH-IMPACT OPERATIONS                             │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute                                          │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes.
4. For write operations or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Most Google Maps API calls are read-only (geocoding, directions, place search).
- API quotas and limits apply — check the Google Cloud Console for your project limits.
- Place IDs are stable but may change over time — always capture fresh IDs from search responses.
- Routing results depend on real-time traffic data when available.
- `snap_to_roads` requires a Google Maps Roads API-enabled project.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-maps`. |
| Missing connection | Google Maps is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-maps. |
| `NOT_FOUND` | Place or location does not exist. Check the place_id or query. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `OVER_QUERY_LIMIT` | API quota exceeded. Wait and retry, or check Google Cloud quotas. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-maps`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [Places API](https://developers.google.com/places/web-service/overview)
- [Directions API](https://developers.google.com/maps/documentation/directions/overview)
- [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-maps-places
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-maps-places)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)