## Description:

Expert guidance on choosing the right Mapbox search tool and parameters for geocoding, POI search, and location discovery

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select the appropriate Mapbox search tool and parameters for geocoding, point-of-interest search, reverse geocoding, local search, and location discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to pass user-provided location or coordinates to Mapbox tools for local results.

Mitigation: Confirm privacy expectations before using precise location data and pass only the location context needed for the search task.

Risk: Mapbox token scope and API quota impact are deployment-dependent, and ETA routing options can add per-result cost.

Mitigation: Confirm Mapbox token scope separately and request ETA or routing parameters only when the user needs travel-time results.

## Reference(s):

- [Advanced Parameters Reference](references/advanced-params.md)
- [Performance, Combining Tools, and Troubleshooting](references/optimization-combining.md)
- [Common Patterns and Workflows](references/workflows.md)
- [Mapbox Search Box API Docs](https://docs.mapbox.com/api/search/search-box/)
- [Category Search API](https://docs.mapbox.com/api/search/search-box/#category-search)
- [Geocoding API](https://docs.mapbox.com/api/search/geocoding/)
- [Category List Resource](https://docs.mapbox.com/api/search/search-box/#category-list)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with JSON and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for Mapbox search workflows; may guide agents to use location or coordinate inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
