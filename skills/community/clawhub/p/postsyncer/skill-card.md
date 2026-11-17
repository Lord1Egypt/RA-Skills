## Description:

Manage and analyze social media posts, media, comments, campaigns, and analytics across connected platforms through PostSyncer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdulmejidshemsuawel](https://clawhub.ai/user/abdulmejidshemsuawel)

### License/Terms of Use:

MIT-0

## Use Case:

External users managing connected social accounts can use this skill to schedule or publish content, organize media, manage comments and campaigns, and review analytics through PostSyncer. Accounts must already be connected in PostSyncer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform account and other delete operations, and selected media may be sent to PostSyncer.

Mitigation: Limit token abilities to the operations you need; confirm deletion targets and review media and destinations before uploading or publishing.

## Reference(s):

- [PostSyncer API Reference](https://docs.postsyncer.com/api-reference/introduction)
- [PostSyncer API Authentication](https://docs.postsyncer.com/essentials/authentication)
- [PostSyncer MCP and OpenClaw setup](https://postsyncer.com/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with JSON API request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflows require connected social accounts and a PostSyncer API token or an authorized MCP connection.]

## Skill Version(s):

2.2.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
