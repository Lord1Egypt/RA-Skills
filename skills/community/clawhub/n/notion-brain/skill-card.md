## Description: <br>
Routes high-value content into a Notion workspace with a quality gate, destination mapping, and Notion MCP write patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to decide whether durable content should be saved to Notion, route it to the right hub or Inbox DB, and produce the Notion MCP write pattern or operator summary for the save. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, overwrite, comment on, or duplicate persistent Notion workspace content. <br>
Mitigation: Limit the Notion integration to specific approved pages and databases, search before creating pages, and require explicit confirmation before any Notion write, comment, memory save, or replace_content operation. <br>
Risk: Broad activation rules can capture low-value, duplicate, or unintended content. <br>
Mitigation: Apply the decision gate before writing, skip trivial or transient content, use Inbox DB for uncertain captures, and avoid excluded health, property, vehicle, or equipment workflows. <br>
Risk: Placeholder Notion IDs can route content to the wrong destination if used unchanged. <br>
Mitigation: Replace every YOUR_* page or data source ID with approved workspace IDs before use and keep private Notion IDs out of shared repositories. <br>


## Reference(s): <br>
- [Notion Brain release page](https://clawhub.ai/zurbrick/notion-brain) <br>
- [MCP command patterns](references/mcp-commands.md) <br>
- [Page map](references/page-map.md) <br>
- [Content templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Compact Markdown summary with Notion MCP command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Notion-flavored Markdown payloads and placeholder page or data source IDs that must be replaced before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
