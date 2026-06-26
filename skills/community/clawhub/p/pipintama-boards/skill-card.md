## Description: <br>
Create, fetch, share, update, export, or change visibility for hosted Pipintama Boards through the MCP server when a user needs a mind map, flowchart, kanban board, or architecture map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create or manage hosted visual boards for planning, brainstorming, process design, task organization, and system architecture mapping. It is most useful when a shareable visual board or PNG export is a better response than prose alone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Board content is sent to Pipintama's hosted service. <br>
Mitigation: Avoid sending sensitive material unless this service is appropriate for the data, and prefer scoped or revocable API keys when available. <br>
Risk: New boards default to shared visibility unless the user asks otherwise. <br>
Mitigation: Ask for private visibility for business, personal, architecture, or other sensitive boards. <br>
Risk: The skill can create shareable viewer and PNG export URLs. <br>
Mitigation: Return only live Pipintama URLs from tool responses and avoid fabricating board or export links. <br>


## Reference(s): <br>
- [Pipintama MCP endpoint](https://api.pipintama.com/mcp) <br>
- [Pipintama MCP health check](https://api.pipintama.com/mcp-health) <br>
- [ClawHub skill page](https://clawhub.ai/davidk2yoyo/pipintama-boards) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Hosted board links, PNG export links, Guidance] <br>
**Output Format:** [Plain text or Markdown with live Pipintama viewer and export URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a hosted viewer URL followed by one short explanation sentence; PNG export URLs are included when useful for image-friendly channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
