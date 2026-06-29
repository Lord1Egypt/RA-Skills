## Description: <br>
Optimizes routes for 2-25 waypoints, provides route details, and can generate map links for multi-stop travel planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan delivery, sales, field service, real estate, mobile business, and tour routes across 2-25 stops. It helps compare optimized stop ordering, route distance, travel time, directions, and optional map outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route planning may send addresses or coordinates to AgentPMT or mapping services. <br>
Mitigation: Use the skill only when external route planning is intended, avoid sensitive locations when possible, and prefer generalized stops when exact addresses are not required. <br>
Risk: Map image links are signed URLs that may expire after seven days. <br>
Mitigation: Present map URLs promptly and regenerate maps when users need fresh links. <br>
Risk: Optimized routes may not be globally optimal for larger route sets. <br>
Mitigation: Treat the route as planning assistance and review route order, timing, and business constraints before operational use. <br>


## Reference(s): <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/multi-location-route-optimizer-w-map) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, URLs, Guidance] <br>
**Output Format:** [Markdown instructions with JSON action schemas, request examples, route details, directions, Google Maps URLs, and map image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optimize_route, get_route_details, and create_route_map actions for 2-25 locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
