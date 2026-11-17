## Description:

Automates GitHub issues, pull request analysis, release creation, repository statistics, and repository health checks for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy825lay-tech](https://clawhub.ai/user/andy825lay-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to automate repository maintenance tasks such as creating and updating issues, reviewing pull requests, creating releases, and collecting repository health signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-backed GitHub write code is intentionally obfuscated, which can make behavior difficult to review before installation.

Mitigation: Review the package before use, install only after accepting the obfuscation risk, and use a fine-grained GitHub token limited to the target repositories.

Risk: The skill's memory-security claim is unsupported in the security evidence.

Mitigation: Avoid broad organization or classic tokens, monitor behavior during initial use, and be prepared to revoke the token if behavior is unexpected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andy825lay-tech/skills/github-automation-pro)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, shell commands, guidance]

**Output Format:** [JSON results and Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token and repository owner/repo configuration for GitHub API operations.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, README, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
