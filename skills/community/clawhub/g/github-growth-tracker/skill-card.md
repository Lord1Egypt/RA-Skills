## Description:

Tracks GitHub repository growth across stars, forks, issues, commits, and watchlist comparisons, then produces periodic trend digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to monitor GitHub repository metrics over time, generate growth digests, and compare their projects with watched repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using setup with a token saves the GitHub personal access token in a local plaintext credentials file.

Mitigation: Prefer passing the token through GITHUB_TOKEN from the agent or shell, and use a fine-grained public-repository read-only token.

## Reference(s):

- [GitHub project homepage](https://github.com/99rebels/github-growth-tracker)
- [Channel Formatting](references/formatting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text digest with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest formatting varies by channel; repository history is retained for up to 90 days.]

## Skill Version(s):

1.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
