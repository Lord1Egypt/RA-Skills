## Description:

Notion API for creating and managing pages, databases, and blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7revor](https://clawhub.ai/user/7revor)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to work with the Notion API for reading, creating, querying, and updating pages, data sources, and content blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a local Notion integration token, which can expose workspace content if stored or shared carelessly.

Mitigation: Use a least-privilege Notion integration, share only required pages or data sources, and store the token with owner-only permissions or a secret manager.

Risk: The documented create, update, and append requests can modify Notion workspace content.

Mitigation: Review any create, update, or append command before running it, especially target IDs and request payloads.

## Reference(s):

- [Notion API documentation](https://developers.notion.com)
- [Notion integrations setup](https://notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Notion API setup guidance, curl commands, endpoint examples, and property payload examples.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
