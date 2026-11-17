## Description:

Publish articles to Notion using cached local copies of the target database's default Notion template when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miraclemin](https://clawhub.ai/user/miraclemin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content teams use this skill to draft, format, publish, search, and update article pages in Notion databases through available Notion MCP tools or the bundled CLI runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion integration token can read and modify Notion content shared with the integration.

Mitigation: Use the least-privileged Notion integration and share only the target database or page with it.

Risk: Update operations can replace existing page content.

Mitigation: Confirm the target page and update mode before running replace or update commands.

Risk: Local token storage can expose credentials if the environment is shared or misconfigured.

Mitigation: Avoid passing tokens on the command line, protect ~/.notion_publish/.env with restrictive permissions, or use a safer secret store.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miraclemin/skills/notion-publisher)
- [Notion API Endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON command output, shell commands, and Notion page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update external Notion pages when configured with a Notion token and a shared target database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
