## Description: <br>
Expert guidance on choosing the right geospatial tool based on problem type, accuracy requirements, and performance needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI assistants use this skill to choose Mapbox MCP Server tools for geospatial tasks. It helps distinguish geometric operations from routing and navigation APIs based on accuracy needs, traffic awareness, scale, and performance constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real location or address data may be sent to Mapbox services when an agent follows recommendations involving search, routing, matrix, isochrone, or optimization APIs. <br>
Mitigation: Review data handling requirements, Mapbox credentials, costs, and rate limits before using the recommended workflows with production or sensitive data. <br>
Risk: Ambiguous requests such as distance, nearby, close, or reachable can lead to the wrong tool category if the agent does not clarify the user's intent. <br>
Mitigation: Clarify whether the user needs straight-line geometry, road-network distance, travel time, or traffic-aware routing before selecting a Mapbox MCP tool. <br>


## Reference(s): <br>
- [Mapbox MCP Server](https://github.com/mapbox/mcp-server) <br>
- [Turf.js Documentation](https://turfjs.org/) <br>
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/) <br>
- [Mapbox Isochrone API](https://docs.mapbox.com/api/navigation/isochrone/) <br>
- [Mapbox Matrix API](https://docs.mapbox.com/api/navigation/matrix/) <br>
- [Mapbox Optimization API](https://docs.mapbox.com/api/navigation/optimization/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with Mapbox MCP tool recommendations, decision matrices, and clarification questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended Mapbox MCP tool names and workflow sequences; does not execute tools or API calls itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
