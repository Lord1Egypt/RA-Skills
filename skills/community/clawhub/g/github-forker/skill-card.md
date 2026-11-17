## Description:

Extracts GitHub repository references from text or images, forks them through the GitHub API, stars the original repositories, and reports the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chat2dev](https://clawhub.ai/user/chat2dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to copy referenced GitHub repositories into the user's GitHub account and summarize fork, star, and error outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GitHub token and can affect the user's GitHub account.

Mitigation: Use a least-privilege or short-lived token and review requested fork operations before execution.

Risk: The skill automatically stars original repositories after successful forks.

Mitigation: Require explicit consent for starring or remove the automatic starring step before normal use.

Risk: The setup guidance shows persistent shell startup storage for GITHUB_TOKEN.

Mitigation: Avoid storing the token in shell startup files; prefer session-scoped or managed secret storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chat2dev/skills/github-forker)
- [curl for Windows](https://curl.se/windows/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call GitHub REST API endpoints with GITHUB_TOKEN and report fork, star, and failure results.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
