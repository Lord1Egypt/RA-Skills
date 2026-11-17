## Description:

Plan place search, geocoding, routing, and map-link workflows across Google Maps, Apple Maps, OpenStreetMap, and other providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, travel planners, and logistics users use this skill to plan provider-aware map workflows for place search, geocoding, routing, ETA checks, static maps, and shareable map links. It helps agents choose providers, normalize map data, manage cost and privacy boundaries, and preview high-impact route or link launches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map tasks may send addresses, coordinates, route endpoints, place queries, or itinerary details to a selected map provider.

Mitigation: Use explicit activation and confirm before live provider calls, route launches, or share links that include sensitive origin, destination, or itinerary data.

Risk: Local files under `~/maps/` can reveal recurring places, provider preferences, and personal routines.

Mitigation: Treat `~/maps/` as sensitive, store only minimal reusable context, and avoid storing API keys, raw itinerary dumps, or sensitive location history by default.

Risk: Paid map providers can incur quota or cost from repeated searches, broad queries, matrix calls, or static-map regeneration.

Mitigation: Bound searches, reuse confirmed provider IDs, cache user-approved recurring origins or destinations, rate-limit retries, and stop on quota errors before sending more requests.

Risk: Ambiguous places, approximate geocodes, coordinate-order mistakes, or straight-line distance assumptions can produce misleading routes or locations.

Mitigation: Normalize provider output, preserve coordinate precision, request missing geography context, use route engines for ETA and travel distance, and preview provider, mode, origin, and destination before launch.

## Reference(s):

- [ClawHub Maps skill page](https://clawhub.ai/ivangdavila/skills/maps)
- [Maps homepage](https://clawic.com/skills/maps)
- [Provider Matrix - Maps](artifact/provider-matrix.md)
- [Normalization Guide - Maps](artifact/normalization-guide.md)
- [Execution Patterns - Maps](artifact/execution-patterns.md)
- [Cost Controls - Maps](artifact/cost-controls.md)
- [Memory Template - Maps](artifact/memory-template.md)
- [Troubleshooting - Maps](artifact/troubleshooting.md)
- [Google Maps API endpoint](https://maps.googleapis.com)
- [Apple Maps link endpoint](https://maps.apple.com)
- [OpenStreetMap Nominatim endpoint](https://nominatim.openstreetmap.org)
- [OSRM public routing endpoint](https://router.project-osrm.org)
- [Mapbox API endpoint](https://api.mapbox.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with structured summaries, map links, provider choices, and inline command or API request examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include normalized place, geocode, route, matrix, or map-link fields; live provider calls and launches require user confirmation for sensitive data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
