## Description: <br>
Generates static map images with markers, optional paths, labels, selectable map types, and hosted image links through AgentPMT remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create static map visualizations for routes, reports, geographic distributions, travel plans, field service locations, and property maps. It is suited to workflows that can send coordinates, labels, and route details to AgentPMT for remote image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map requests may send coordinates, labels, and route details to AgentPMT for remote processing. <br>
Mitigation: Use the skill only when the user approves external processing, and avoid private homes, sensitive sites, protected locations, or identifying labels unless they are necessary and approved. <br>
Risk: Generated map images are exposed through signed URLs that remain available for 7 days. <br>
Mitigation: Treat generated links as shareable artifacts, avoid including sensitive location data, and expire or replace links in downstream materials when they are no longer needed. <br>
Risk: Requests can fail or produce unclear responses when schema, authentication, or payment requirements are not satisfied. <br>
Mitigation: Check the live schema when parameters are unclear, keep credentials out of prompts and logs, and retry only after fixing schema, authentication, or payment issues. <br>


## Reference(s): <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/map-generator-with-markers) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/map-generator-with-markers) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text, markdown] <br>
**Output Format:** [Markdown instructions with JSON request and response examples for remote map-generation calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote calls can return a signed URL, base64 PNG image data, file identifier, file size, point count, and map settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
