## Description:

Common patterns for building store locators, restaurant finders, and location-based search applications with Mapbox. Covers marker display, filtering, distance calculation, and interactive lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and implement store locators, restaurant finders, and location-based search workflows with Mapbox GL JS. It provides patterns for marker strategies, GeoJSON location data, filtering, distance sorting, directions, synchronized lists, layout, performance, accessibility, and React variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples may use unsafe HTML rendering for store names, addresses, phone numbers, website links, or popup content.

Mitigation: Use safe DOM construction such as textContent, createElement, setDOMContent, validated URLs, and no inline JavaScript handlers before adapting examples for production.

Risk: Geolocation and directions workflows may under-disclose precise location sharing and coordinate transmission.

Mitigation: Show clear user-facing disclosure before requesting precise location and before sending coordinates to Mapbox for directions, and provide a non-geolocation fallback where practical.

## Reference(s):

- [HTML Markers and Clustering](references/markers.md)
- [Search and Filter](references/search-filter.md)
- [Geolocation, Distance and Directions](references/geolocation-directions.md)
- [Styling and Layout](references/styling-layout.md)
- [Performance and Accessibility](references/optimization-a11y.md)
- [Variations and React](references/variations-react.md)
- [Turf.js](https://turfjs.org/)
- [Mapbox GL JS API](https://docs.mapbox.com/mapbox-gl-js/)
- [Mapbox GL JS Interactions API Guide](https://docs.mapbox.com/mapbox-gl-js/guides/user-interactions/interactions/)
- [GeoJSON Specification](https://geojson.org/)
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [Mapbox Store Locator Tutorial](https://docs.mapbox.com/help/tutorials/building-a-store-locator/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript, JSON, HTML, CSS, React, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation patterns and examples that require developer review before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
