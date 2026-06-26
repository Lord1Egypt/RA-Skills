## Description: <br>
Expert guidance on choosing the right Mapbox search tool and parameters for geocoding, POI search, and location discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose among Mapbox search, category search, and reverse geocoding workflows, then apply appropriate parameters for location discovery, POI lookup, and geocoding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nearby search workflows can involve precise user location. <br>
Mitigation: Prefer a city, ZIP code, or approximate area unless precise location is necessary, and avoid reuse or storage of location data unless the user clearly agrees. <br>
Risk: ETA and routing-related search parameters can increase API usage and cost. <br>
Mitigation: Request ETA only when travel time or routing is needed, and otherwise use search results with offline distance or bearing calculations where appropriate. <br>


## Reference(s): <br>
- [Advanced Parameters Reference](artifact/references/advanced-params.md) <br>
- [Performance, Combining Tools, and Troubleshooting](artifact/references/optimization-combining.md) <br>
- [Common Patterns and Workflows](artifact/references/workflows.md) <br>
- [Mapbox Search Box API Docs](https://docs.mapbox.com/api/search/search-box/) <br>
- [Category Search API](https://docs.mapbox.com/api/search/search-box/#category-search) <br>
- [Geocoding API](https://docs.mapbox.com/api/search/geocoding/) <br>
- [Category List Resource](https://docs.mapbox.com/api/search/search-box/#category-list) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with JSON and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Mapbox search tool selection, parameter recommendations, workflow patterns, and anti-patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
