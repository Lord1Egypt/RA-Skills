## Description:

Backup Clawdbot workspace and config to GitHub with git-crypt encryption. Use for daily automated backups or manual backup/restore operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louzhixian](https://clawhub.ai/user/louzhixian)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure encrypted GitHub backups for Clawdbot workspace and configuration directories, and to run manual or scheduled backup and restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated backups can upload broad workspace and configuration data, including secrets and sessions, to GitHub.

Mitigation: Use private repositories, review staged files before enabling scheduled backups, and consider excluding live credentials, sessions, identity, and node state.

Risk: Sensitive files may be committed before git-crypt protection is correctly configured.

Mitigation: Verify git-crypt setup and encrypted path rules before the first commit, and add secret scanning or an allowlist for backup repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, backup, and restore instructions for git and git-crypt workflows.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
