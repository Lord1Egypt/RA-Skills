## Description:

Fetches public GitHub Trending repositories for daily, weekly, or monthly periods and summarizes repository name, language, stars, description, and URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to quickly inspect public GitHub Trending repositories over daily, weekly, or monthly windows for discovery, reporting, or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts GitHub's public trending page when invoked.

Mitigation: Use it only in environments where outbound access to GitHub is allowed and expected.

Risk: Results can fail or become incomplete if GitHub changes the Trending page structure or applies rate limiting.

Mitigation: Review command output before relying on it and avoid high-frequency polling.

## Reference(s):

- [Github Trending ClawHub release](https://clawhub.ai/jiangzhiyu/skills/github-trending)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown-style terminal output or JSON, depending on invocation and release behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live public data from GitHub Trending and does not require authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
