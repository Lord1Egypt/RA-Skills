## Description:

Universal travel planning skill for OpenClaw agents. Plan itineraries, check weather, discover attractions, and estimate budgets through natural conversation, with no API key required for core features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to add destination-aware travel planning to OpenClaw agents, including itineraries, weather summaries, attraction discovery, cultural tips, packing suggestions, and budget estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destination data is sent to public APIs for geocoding, weather, and travel guide lookups.

Mitigation: Review destination privacy requirements before use, avoid submitting sensitive exact addresses when unnecessary, and disclose public API use to users where appropriate.

Risk: The local SQLite cache can reveal searched destinations, including exact addresses if users provide them.

Mitigation: Store the cache in a protected location with TOUR_PLANNER_CACHE_PATH, clear the database when needed, and avoid shared deployments unless cache access is controlled.

Risk: Broad deployment may need dependency review and input limits.

Mitigation: Update or pin dependencies, audit the native better-sqlite3 dependency during installation, and add runtime input limits before shared or production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asif2bd/skills/openclaw-tour-planner)
- [OpenCLAW Tour Planner Website](https://openclaw.tours)
- [OpenCLAW Tour Planner Docs](https://openclaw.tours/docs)
- [Nominatim Search API](https://nominatim.org/release-docs/develop/api/Search/)
- [Open-Meteo Forecast API](https://open-meteo.com/en/docs#weathervariables)
- [Wikivoyage MediaWiki API](https://en.wikivoyage.org/w/api.php)
- [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown itineraries and weather or budget summaries, with JSON-compatible itinerary structures for agent processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include destination geocoding, weather summaries, attraction lists, cultural tips, packing lists, budget ranges, and emergency numbers.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
