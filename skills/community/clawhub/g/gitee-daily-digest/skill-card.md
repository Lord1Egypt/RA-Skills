## Description:

Use this skill when the user asks for a daily summary, today's to-dos, "what's on my plate today", "daily digest", "daily-digest", "show my notifications", "pending PRs and issues". Requires Gitee MCP Server to be configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Gitee users use this skill to aggregate unread notifications, pending pull requests, and open issues into a concise daily work digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Gitee notifications, user identity, pull requests, and issues to prepare a daily digest.

Mitigation: Install and invoke it only when a Gitee-based digest is intended, and confirm ambiguous daily-summary requests before fetching account or repository data.

## Reference(s):

- [Daily Digest on ClawHub](https://clawhub.ai/oschina/skills/gitee-daily-digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown daily digest with sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Gitee MCP Server access to read notifications, pull requests, issues, and user identity.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
