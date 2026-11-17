## Description:

Convert a private repository to public open-source by sanitizing personal information, cleaning history, and preparing it for public release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jini92](https://clawhub.ai/user/jini92)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill when preparing a private repository for a normal open-source release. It guides repository scanning, sanitization, history handling, publication, and post-release verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact repository publication commands can force-push, delete branches, or make a repository public before the target state is confirmed.

Mitigation: Require explicit approval after verifying the GitHub owner, repository, remote URL, current branch, backup state, and exact diff/history to be published.

Risk: Repository sanitization may miss sensitive files or history entries if release scans are incomplete.

Mitigation: Run final sensitive-string scans, confirm ignored artifacts are excluded, inspect git history, and verify the remote URL contains no token before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jini92/skills/opensource-release)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell, git, and GitHub CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include repository sanitization checklists, command sequences, and verification steps.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
