## Description:

Notion integration for OpenClaw. Manage pages, databases, and blocks via AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an OpenClaw agent manage Notion workspace content, including pages, databases, blocks, and search. It is suited for workflows where Notion resources are intentionally shared with a dedicated integration token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and archive Notion pages and add database entries.

Mitigation: Use a dedicated low-privilege Notion integration token shared only with the specific pages and databases this skill should access, and require explicit confirmation before archive/delete or bulk update actions.

Risk: The README recommends installing uv with a curl-to-shell command.

Mitigation: Install uv through a trusted package manager, or inspect and verify the installer before running it.

Risk: The Notion token grants access to workspace content that has been shared with the integration.

Mitigation: Store NOTION_TOKEN securely, avoid exposing it in logs or shell history, and rotate or revoke it if it may have been exposed.

## Reference(s):

- [Notion API Reference](https://developers.notion.com/reference/intro)
- [Notion Integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown instructions with CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and NOTION_TOKEN; command output depends on Notion API permissions and shared workspace resources.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
