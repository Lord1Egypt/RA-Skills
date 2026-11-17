## Description:

Notion API for creating and managing pages, databases, blocks and enhanced markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fental](https://clawhub.ai/user/fental)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to guide agents in creating, reading, updating, and querying Notion pages, data sources, blocks, and Markdown page content through the Notion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Notion integration token can grant access to pages or databases shared with the integration.

Mitigation: Limit the integration to the minimum required Notion resources and permissions before using the skill.

Risk: The setup example stores the Notion token in a local plaintext file.

Mitigation: Store the token with owner-only permissions or in a credential manager.

Risk: Markdown replacement operations can overwrite or remove page content, especially when using replace_content or allow_deleting_content.

Mitigation: Review target page content and request payloads before execution, prefer narrow search-and-replace updates where possible, and avoid allow_deleting_content unless deletion is intended.

## Reference(s):

- [Notion Developers](https://developers.notion.com)
- [Notion integrations setup](https://notion.so/my-integrations)
- [ClawHub skill release page](https://clawhub.ai/fental/skills/notion-enhanced-markdown)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with curl command examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion API key and access to shared pages or data sources.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
