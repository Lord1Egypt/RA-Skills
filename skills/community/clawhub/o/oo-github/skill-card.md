## Description:

Use this skill for GitHub requests to read, create, update, or delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read and manage GitHub repositories, issues, pull requests, releases, and related data through their connected GitHub account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run downloaded installer code without clearly requiring approval for local changes; the downloaded contents and hosted-service behavior were not verified.

Mitigation: Review and install a verified CLI release yourself, and require approval before any setup changes.

Risk: Automatic skill synchronization and broad GitHub permissions may allow more access or changes than needed.

Mitigation: Check automatic synchronization settings and grant only the GitHub permissions needed.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [GitHub REST API documentation](https://docs.github.com/en/rest)
- [ClawHub GitHub skill release](https://clawhub.ai/oomol/skills/oo-github)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and oo CLI commands with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payloads follow the selected action schema; changes to GitHub require confirmation.]

## Skill Version(s):

1.0.12 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
