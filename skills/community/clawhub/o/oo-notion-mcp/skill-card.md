## Description:

Notion MCP (notion.so). Use this skill for ANY Notion MCP request — reading, creating, and updating data. Whenever a task involves Notion MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers working with an OOMOL-connected Notion workspace can search and read pages, manage comments, inspect tool access, create pages, and update page content through Notion MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded software that the release evidence says remains unverified, and automatic agent-skill changes are not disclosed.

Mitigation: Review the installation, use a verified CLI release, approve local setup changes explicitly, and consider setting OO_SKILLS_SYNC_DISABLED=1.

Risk: Creating comments or pages and updating pages can change Notion content.

Mitigation: Limit the connected Notion permissions and confirm the exact payload and effect before running each write action.

## Reference(s):

- [Notion MCP documentation](https://developers.notion.com/docs/mcp)
- [Notion MCP homepage](https://www.notion.so)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-notion-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured JSON tool results with Notion page content in Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create or update Notion content require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
