## Description:

Integrate with Notion API v1 to search, read, create, update, comment on, and archive pages and databases within a Notion workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolfun](https://clawhub.ai/user/gaolfun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to let an agent search, read, create, update, comment on, and archive Notion pages and databases through the Notion API after access is explicitly shared with an integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify, comment on, or archive Notion workspace content.

Mitigation: Require a preview and explicit user confirmation before page updates, comments, database changes, or archiving actions.

Risk: A long-lived Notion integration token can expose any pages or databases shared with the integration.

Mitigation: Store the token as a secret, avoid pasting it into chat, and share only the narrowest necessary Notion pages or databases with the integration.

Risk: Database schema changes or broad integration sharing can cause failed writes or unintended workspace access.

Mitigation: Fetch the current database schema before writes and keep Notion sharing scoped to the specific workspace content needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaolfun/skills/notion-integration)
- [Notion integrations setup](https://www.notion.so/profile/integrations)
- [Notion API v1 base endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, JSON request bodies, shell commands, and structured success or error summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Notion object IDs, page or database URLs, timestamps, API error codes, and retry or access suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact body lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
