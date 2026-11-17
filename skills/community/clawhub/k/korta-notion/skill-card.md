## Description:

Notion API for creating and managing pages, databases, and blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landercortazarromero](https://clawhub.ai/user/landercortazarromero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Notion API access and issue cURL requests for searching, reading, creating, and updating Notion pages, data sources, and blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup stores a Notion token in a local plaintext file.

Mitigation: Create a minimally scoped Notion integration, restrict shared pages and data sources, and store the token with owner-only permissions or in a secret manager.

Risk: The generated API examples can modify Notion workspace content when used with write access.

Mitigation: Test requests against non-critical pages or data sources first, review request bodies before execution, and grant only the permissions required for the intended task.

## Reference(s):

- [Notion API documentation](https://developers.notion.com)
- [Notion integrations setup](https://notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides Notion API request patterns and setup steps; users supply their own workspace IDs, page IDs, data source IDs, and API token.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
