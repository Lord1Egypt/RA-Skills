## Description: <br>
Common patterns for building store locators, restaurant finders, and location-based search applications with Mapbox. Covers marker display, filtering, distance calculation, and interactive lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Mapbox-based store locators, restaurant finders, and location-search applications with marker strategies, filtering, distance sorting, interactive lists, and optional directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location-aware examples can expose or retain precise user coordinates and directions requests may send coordinates to Mapbox. <br>
Mitigation: Add an explicit 'Use my location' action, explain why location is needed, disclose coordinate sharing for directions, and avoid retaining precise coordinates unnecessarily. <br>
Risk: Popup and listing snippets use raw HTML rendering patterns that can be unsafe when store data comes from users, CMS feeds, partners, or other untrusted sources. <br>
Mitigation: Render untrusted store fields with textContent, DOM construction, or a trusted sanitizer before production use. <br>
Risk: Mapbox access tokens used by locator applications can be copied or misused if left unrestricted. <br>
Mitigation: Use restricted Mapbox tokens with appropriate URL, domain, and scope limits. <br>


## Reference(s): <br>
- [HTML Markers, Symbol Layers, and Clustering](references/markers.md) <br>
- [Search and Filter](references/search-filter.md) <br>
- [Geolocation, Distance, and Directions](references/geolocation-directions.md) <br>
- [Styling and Layout](references/styling-layout.md) <br>
- [Performance and Accessibility](references/optimization-a11y.md) <br>
- [Variations and React](references/variations-react.md) <br>
- [Turf.js](https://turfjs.org/) <br>
- [Mapbox GL JS API](https://docs.mapbox.com/mapbox-gl-js/) <br>
- [Mapbox GL JS Interactions API Guide](https://docs.mapbox.com/mapbox-gl-js/guides/user-interactions/interactions/) <br>
- [GeoJSON Specification](https://geojson.org/) <br>
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/) <br>
- [Mapbox Store Locator Tutorial](https://docs.mapbox.com/help/tutorials/building-a-store-locator/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, HTML/CSS, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mapbox GL JS v3.x and @turf/turf for the documented patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
