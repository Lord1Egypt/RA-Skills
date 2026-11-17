## Description:

Notion API for creating and managing pages, databases, and blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhuanlaptrinh](https://clawhub.ai/user/nhuanlaptrinh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through common Notion API workflows, including creating, reading, updating, and querying pages, data sources, and blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to use a Notion integration token that can access shared pages and data sources.

Mitigation: Store the token with owner-only permissions, grant the narrowest practical Notion integration permissions, avoid exposing the token in shell history, and revoke or rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nhuanlaptrinh/skills/nhuann8n)
- [Notion API documentation](https://developers.notion.com)
- [Notion integrations setup](https://notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token provided through NOTION_API_KEY or an equivalent local secret file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
