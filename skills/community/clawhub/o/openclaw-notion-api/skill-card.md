## Description:

Guides agents through Notion API operations for pages, data sources, blocks, and direct file uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ionepub](https://clawhub.ai/user/ionepub)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to construct Notion API requests for creating, reading, updating, querying, and uploading content in a connected Notion workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion integration token can expose sensitive or business-critical workspace data if stored in plaintext or granted broad access.

Mitigation: Use a least-privilege Notion integration, share only the required pages or databases, and prefer an OS keychain or secret manager instead of a plaintext token file.

Risk: Create, update, append, and upload commands can change workspace content or attach unintended local files.

Mitigation: Confirm page IDs, database IDs, and local file paths before running write or upload commands.

## Reference(s):

- [Notion API documentation](https://developers.notion.com)
- [ClawHub skill page](https://clawhub.ai/ionepub/skills/openclaw-notion-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with curl command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Notion API headers, endpoint paths, setup steps, and example request bodies.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
