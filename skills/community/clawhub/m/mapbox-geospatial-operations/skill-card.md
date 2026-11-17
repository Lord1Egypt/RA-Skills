## Description:

Expert guidance on choosing the right geospatial tool based on problem type, accuracy requirements, and performance needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistants use this skill to choose appropriate Mapbox MCP Server geospatial tools for distance, routing, containment, service-area, optimization, and shape-analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mapbox API-backed workflows can involve addresses, coordinates, GPS traces, or route queries.

Mitigation: Review whether the intended use permits sharing location data with Mapbox, minimize sensitive location details, and prefer offline geometric tools when routing data is not needed.

Risk: Choosing a geometric tool for a routing or travel-time question can produce misleading distance or reachability guidance.

Mitigation: Clarify whether the user needs straight-line distance, road distance, travel time, or traffic awareness before recommending a tool.

Risk: High-frequency geofencing through agent-mediated MCP calls may add unnecessary latency or operational overhead.

Mitigation: Use Turf.js directly in-process for hot-path containment checks and reserve MCP tools for zone definition, rerouting, or visualization.

## Reference(s):

- [Mapbox Geospatial Operations on ClawHub](https://clawhub.ai/mapbox/skills/mapbox-geospatial-operations)
- [Mapbox Publisher Profile](https://clawhub.ai/user/mapbox)
- [Mapbox MCP Server](https://github.com/mapbox/mcp-server)
- [Turf.js Documentation](https://turfjs.org/)
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [Mapbox Isochrone API](https://docs.mapbox.com/api/navigation/isochrone/)
- [Mapbox Matrix API](https://docs.mapbox.com/api/navigation/matrix/)
- [Mapbox Optimization API](https://docs.mapbox.com/api/navigation/optimization/)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance with tool recommendations and decision frameworks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mapbox MCP tool names and recommended sequencing for geospatial workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
