## Description: <br>
Location Street View & Satellite Imagery gets Street View panoramas, satellite or aerial imagery, and geocoding results through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to geocode addresses or coordinates and retrieve Street View, satellite, roadmap, hybrid, or terrain imagery for location verification, property assessment, travel planning, and geographic validation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends addresses or coordinates to AgentPMT for paid remote processing, and generated image links may remain available for up to 7 days. <br>
Mitigation: Use the skill only for location data appropriate for AgentPMT processing, avoid highly sensitive home, workplace, or travel locations unless necessary, and account for the 7-day signed URL availability window. <br>


## Reference(s): <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/location-street-view-satellite-imagery) <br>
- [Action Schema](schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls return geocoding data, signed image URLs, base64 image data, and imagery metadata depending on the selected action.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
