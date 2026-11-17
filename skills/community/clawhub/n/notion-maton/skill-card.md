## Description:

Access and manage Notion workspaces through Maton-managed OAuth to search pages, query data sources and databases, manage pages and blocks, and retrieve user information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to have an agent generate Notion API requests through Maton's OAuth gateway for workspace search, database and data source operations, page and block management, and user lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Notion workspace access is concentrated through a third-party gateway.

Mitigation: Install only when Maton is trusted with the Notion workspace content and operations sent through the gateway, and use the least-privileged Notion connection possible.

Risk: Generated requests can archive pages, delete blocks, or change database and data source schemas.

Mitigation: Require explicit confirmation before archive, delete, or schema-changing operations.

Risk: Troubleshooting guidance may expose the Maton API key if credential output is shared.

Mitigation: Do not run or share output from commands that print MATON_API_KEY; rotate the key if it has already been exposed.

## Reference(s):

- [ClawHub Notion Skill](https://clawhub.ai/otman-ai/skills/notion-maton)
- [otman-ai Publisher Profile](https://clawhub.ai/user/otman-ai)
- [Maton](https://maton.ai)
- [Maton Connection Management](https://ctrl.maton.ai)
- [Notion API](https://api.notion.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cURL examples and request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton API key, a Notion OAuth connection, and the Notion-Version request header.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
