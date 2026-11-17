## Description:

Optimizes routes for 2-25 waypoints, provides route details, and can generate static map links for AgentPMT-hosted route-planning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to plan efficient multi-stop routes for deliveries, sales visits, service calls, property tours, mobile businesses, or tours. Agents can request optimized stop ordering, directions, route totals, map images, and Google Maps navigation URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route requests may send sensitive locations, labels, or related operational details to AgentPMT or mapping services.

Mitigation: Submit only the addresses and labels needed for routing, avoid personal or sensitive facility details, and review data-handling requirements before use.

Risk: Related setup instructions document unpinned npx installation commands.

Mitigation: Prefer pinned or verified installation methods and review setup packages before running install commands.

Risk: The nearest-neighbor optimization approach may produce a route that is efficient but not globally optimal.

Mitigation: Review high-value or safety-critical routes before dispatch and compare results against operational constraints.

## Reference(s):

- [Action schema](artifact/schema.md)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/multi-location-route-optimizer-w-map)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/multi-location-route-optimizer-w-map)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON route data and map URLs, typically summarized for users in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 2-25 locations; generated map image signed URLs expire after 7 days; route optimization uses a nearest-neighbor algorithm and may not be globally optimal.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
