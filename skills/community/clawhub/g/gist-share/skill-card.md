## Description:

Post content to GitHub Gist and get back a shareable URL. Rich context sharing between agents, operators, and humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ragesaq](https://clawhub.ai/user/ragesaq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to publish markdown or text context to GitHub Gist and return a shareable URL for handoffs, reports, plans, logs, or future-session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish arbitrary user or agent content externally through GitHub Gist, and public gists are visible to anyone with access to the URL.

Mitigation: Review and redact content before upload, and use secret gists or access-controlled storage for non-public material.

Risk: The setup guidance includes persistent shell-profile token storage for a GitHub token.

Mitigation: Prefer short-lived or credential-manager-backed authentication, avoid storing PATs in shell profile files, and grant only the minimum gist scope.

## Reference(s):

- [Gist Share homepage](https://github.com/PsiClawOps/gist-share)
- [ClawHub skill page](https://clawhub.ai/ragesaq/skills/gist-share)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a returned Gist URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub CLI authentication and a GitHub token with gist scope before posting.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
