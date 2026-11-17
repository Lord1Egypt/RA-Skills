## Description:

PandaDoc (pandadoc.com). Use this skill for ANY PandaDoc request — reading, creating, updating, and deleting data. Whenever a task involves PandaDoc, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to read PandaDoc documents and templates, manage contacts and folders, and create or update documents, templates, attachments, and webhooks through a connected PandaDoc account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified downloaded software without a separate approval step.

Mitigation: Inspect the CLI release and installer first, and require approval before running downloaded installers; disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if appropriate.

## Reference(s):

- [PandaDoc homepage](https://www.pandadoc.com)
- [PandaDoc API documentation](https://developers.pandadoc.com/reference/about)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [PandaDoc ClawHub release](https://clawhub.ai/oomol/skills/oo-pandadoc)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON connector payloads and results, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions are safe to run directly; writes require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
