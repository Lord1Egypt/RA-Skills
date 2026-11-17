## Description:

Professional changelog and release notes generator for client-facing software releases and updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release managers, and agency teams use this skill to capture project changes, import conventional git commits, and produce audience-specific changelogs, client emails, Telegram-style updates, and release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed nex-changelog wrapper can run a same-named script from the current directory.

Mitigation: Review or fix the wrapper before installation, and run the command only from trusted directories until the wrapper executes only the intended installed script.

Risk: Client-facing and public outputs can include internal changelog data.

Mitigation: Review generated email, Telegram, public changelog, and release-note output before sharing externally, and verify audience filters for sensitive entries.

Risk: Imported commit messages, internal notes, client emails, repository paths, and security-fix descriptions may contain sensitive information.

Mitigation: Avoid adding secrets or confidential details, keep the local data directory access-restricted, and sanitize entries before export or external publication.

## Reference(s):

- [Nex AI homepage](https://nex-ai.be)
- [Keep a Changelog](https://keepachangelog.com/)
- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-changelog)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text CLI output, Markdown changelogs, client-facing message text, and JSON structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated release communication is based on locally stored project, release, entry, and git commit data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
