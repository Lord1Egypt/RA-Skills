## Description:

A professional notes-sync CLI skill for managing Markdown note vaults with batch operations, multi-vault workflows, templates, Git synchronization, LLM-assisted organization, and cross-device sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers, developers, researchers, operations teams, and compliance teams use this skill to plan and execute Markdown note-vault management workflows. It helps produce CLI commands and configuration guidance for bulk note operations, Git-backed synchronization, LLM-assisted organization, templates, health checks, and cross-device workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad local file and shell actions, including note deletion, cleanup, and bulk edits.

Mitigation: Limit use to explicit note-vault tasks, require dry-run previews, and require clear confirmation before delete, cleanup, or apply operations.

Risk: Git synchronization and LLM-assisted organization can send note content or metadata to a remote repository or external API.

Mitigation: Keep Git sync and LLM features disabled unless that data flow is intended, and review credentials, remotes, and API configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notes-sync-cli-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for local file changes, deletion, Git synchronization, LLM processing, and generated reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
