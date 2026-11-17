## Description:

Production-ready Notion API client for SaaS workflows. Create/read/update pages, query data sources, append blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomas-mikula](https://clawhub.ai/user/tomas-mikula)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate on Notion workspaces from SaaS workflows, including searching content, reading pages, querying data sources, and creating or updating pages, blocks, and data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify live Notion workspace data.

Mitigation: Use a minimal-scope Notion API key and review write requests before execution.

Risk: Notion credentials may be exposed if pasted into chat transcripts or logs.

Mitigation: Provide credentials through the configured secret path and avoid placing real tokens in conversation text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomas-mikula/skills/notion-manager)
- [Publisher profile](https://clawhub.ai/user/tomas-mikula)
- [Author website](https://FrontendAccelerator.com)
- [Notion API endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [Structured JSON with status, data, metadata, and error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token supplied through NOTION_API_KEY or auth.notionApiKey.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
