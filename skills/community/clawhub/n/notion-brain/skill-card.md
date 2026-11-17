## Description:

Route high-value content into a Notion workspace with a quality gate, destination mapping, and exact MCP write patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to decide whether durable content should be saved to Notion, choose the right destination, shape the content, and execute the appropriate Notion MCP write pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive or confidential content to Notion and workspace memory.

Mitigation: Require explicit confirmation that shows the destination and operation type, limit Notion permissions to intended pages and databases, and avoid saving security, finance, personal, or confidential content unless explicitly approved.

Risk: The raw Comments API path may bypass the safer native Notion MCP workflow.

Mitigation: Remove or govern the Comments API path before use, or require separate approval when comments are added.

## Reference(s):

- [Notion Brain release page](https://clawhub.ai/zurbrick/skills/notion-brain)
- [Notion Brain - Page Map](references/page-map.md)
- [Notion Brain - Templates](references/templates.md)
- [Notion Brain - MCP Commands](references/mcp-commands.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration]

**Output Format:** [Operator summary with Notion-flavored Markdown and MCP command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Notion pages and database items after destination and operation confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
