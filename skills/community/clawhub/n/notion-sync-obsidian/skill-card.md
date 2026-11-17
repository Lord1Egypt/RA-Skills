## Description:

Automatically syncs Notion articles to a local Obsidian directory, with scheduled checks, full content export, and smart title extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hawkvan](https://clawhub.ai/user/hawkvan)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and Obsidian users use this skill to configure an agent-managed workflow that checks Notion for recently edited pages and exports them as Markdown files into an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says installation and credential-handling guidance expose users to avoidable high-impact risk.

Mitigation: Review the skill before installing, avoid curl-to-bash installation unless independently trusted and verified, and test first with a disposable Obsidian vault.

Risk: The skill requires a Notion integration token and local vault path, and scripts may display a token prefix in command output.

Mitigation: Store the Notion token outside shared or backed-up directories, avoid logged or recorded execution environments until token-prefix printing is removed, and grant the Notion integration access only to the pages or databases intended for sync.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hawkvan/skills/notion-sync-obsidian)
- [Publisher profile](https://clawhub.ai/user/hawkvan)
- [Notion API Guide](references/NOTION_API_GUIDE.md)
- [Notion API Documentation](https://developers.notion.com)
- [Notion Integrations](https://notion.so/my-integrations)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports Notion page content into local Markdown files organized for an Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
