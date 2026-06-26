# Execution Patterns - Maps

Use these patterns to keep map behavior deterministic and reviewable.

## Place Search Pattern

1. Confirm the search text and missing geography context.
2. Pick provider based on detail needs, cost, and privacy.
3. Search for a small bounded result set.
4. Compare top candidates by locality, type, and status.
5. Open or share only after the user approves the right candidate.

## Forward Geocoding Pattern

1. Expand the address with city, region, postal code, and country when available.
2. Request provider output and capture confidence or match type.
3. Return normalized coordinates plus the formatted address.
4. If the result is approximate, say so explicitly.

## Reverse Geocoding Pattern

1. Preserve full input precision.
2. Call a provider that reports confidence or granularity.
3. Return the nearest address plus locality context.
4. Warn if the match is approximate or snapped to a road segment.

## Route Pattern

1. Confirm origin, destination, travel mode, and unit expectations.
2. Decide whether the user needs a structured result, an open map, or both.
3. Use a route engine for ETA and actual distance.
4. Preview final provider, route mode, and major assumptions before launch.

## Matrix or Multi-Stop Pattern

1. Deduplicate repeated origins or destinations before calling the API.
2. Use matrix endpoints only when pair counts justify them.
3. Record returned waypoint order and unit assumptions.
4. If the provider cannot optimize waypoints, say so before computing a fake answer.

## Map Link or App Launch Pattern

1. Build the final URL after the correct place or route is chosen.
2. Show the provider, route mode, and sensitive fields before execution.
3. Require explicit confirmation for share links, bulk opens, or route changes.
4. Summarize the expected visible result after launch.
