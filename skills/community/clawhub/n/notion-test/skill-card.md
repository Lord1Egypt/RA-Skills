## Description:

Notion API for creating and managing pages, databases, and blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfish](https://clawhub.ai/user/qfish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to create, read, update, and query Notion pages, data sources, and blocks through the Notion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Notion token may be stored in local plaintext without permission safeguards.

Mitigation: Create a narrowly scoped Notion integration, share only required pages or data sources, store the token with owner-only permissions or a secret manager, avoid exposing it in shell history, and rotate it if exposure is suspected.

Risk: API commands can read or change connected Notion pages, data sources, and blocks.

Mitigation: Review target IDs and request payloads before execution, and test commands against non-sensitive workspace content first.

## Reference(s):

- [Notion API documentation](https://developers.notion.com)
- [Notion integration setup](https://notion.so/my-integrations)
- [ClawHub skill release](https://clawhub.ai/qfish/skills/notion-test)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes curl examples for Notion API requests; does not generate files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
