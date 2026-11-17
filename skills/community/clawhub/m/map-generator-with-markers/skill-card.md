## Description:

Map Generator With Markers helps agents generate static map images with markers, optional paths, labels, and roadmap, satellite, hybrid, or terrain views through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to create static route maps, location marker visuals, property maps, geographic data summaries, and presentation-ready map images from latitude and longitude inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinates, addresses, routes, and property locations may be sensitive because requests are sent to AgentPMT and generated images are retained for 7 days.

Mitigation: Send only the minimum location data needed for the task, avoid unnecessary sensitive locations, and account for the 7-day retention window before sharing generated links.

Risk: The skill relies on AgentPMT-hosted remote tool calls, so use outside the intended map-generation workflow may send data to a third-party service.

Mitigation: Use the skill only when an AgentPMT map product call is intended, and review setup and invocation routes before production use.

Risk: Fresh endpoint, schema, setup, or example details may change after publication.

Mitigation: For production integrations, fetch the live schema or reinstall the skill when the artifact freshness guidance indicates it is stale.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/map-generator-with-markers)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/map-generator-with-markers)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown guidance with JSON request examples and structured response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated map responses can include a signed URL, base64 PNG image data, a file identifier, image size, point count, and rendering settings; generated images are retained for 7 days.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
