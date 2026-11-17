## Description:

Convert Markdown to Notion blocks with full format support. Handles bold, italic, strikethrough, inline code, headings, lists, tables, callouts, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maweis1981](https://clawhub.ai/user/maweis1981)

### License/Terms of Use:

MIT

## Use Case:

Developers, workspace operators, and content authors use this skill to create or append Notion pages from Markdown while preserving common Markdown formatting as Notion blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion integration token can expose or modify workspace content if it has broader access than needed.

Mitigation: Use a Notion integration token with the smallest required permissions, share only target pages with it, and store it in an environment variable or secret manager.

Risk: Create and append commands write content to Notion pages.

Mitigation: Run with --dry-run before modifying important workspace content and verify the parent or target page ID before execution.

Risk: A plaintext ~/.config/notion/api_key file can expose the Notion API key to other local users.

Mitigation: Restrict the config file permissions to the current user when file-based credential storage is used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maweis1981/skills/notion-md)
- [Notion block API reference](https://developers.notion.com/reference/block)
- [Notion integrations setup](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, append, list, or preview Notion page operations when configured with a Notion API key and parent page ID.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
