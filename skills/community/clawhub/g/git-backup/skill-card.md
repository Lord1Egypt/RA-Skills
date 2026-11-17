## Description:

Backs up an agent workspace to a GitHub repository through token discovery, repository setup, commits, pushes, and scheduled backup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run Git-based backups of an agent workspace to GitHub, including first-time setup, recurring commits, and recovery steps when credentials or remotes fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad GitHub credentials may be requested, discovered, or stored in locations that expose repository access.

Mitigation: Use least-privilege GitHub tokens, do not provide PATs in chat, remove tokens from remote URLs, and store credentials only in approved secret storage.

Risk: Silent scheduled backups can upload large parts of the workspace without review.

Mitigation: Disable silent scheduled pushes unless explicitly approved, use a reviewed backup allowlist, and run a secret scan before uploading workspace files.

Risk: The artifact includes a deprecation note indicating the backup workflow was merged into another maintenance skill.

Mitigation: Confirm the intended install target and prefer the maintained replacement if this standalone release is obsolete.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/netanel-abergel/skills/git-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Git and GitHub API command examples plus scheduled backup configuration guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
