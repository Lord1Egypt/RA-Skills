## Description:

Provides Korean web and Naver-specific search, including news, blogs, local places, and DataLab trends and shopping insights through an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isnow890](https://clawhub.ai/user/isnow890)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other OpenClaw users use this skill to find and summarize Korean-language sources, Naver local information, and DataLab search or shopping trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned third-party npm MCP server runs with Naver API credentials.

Mitigation: Review the skill and use a pinned, vetted server version before installation.

Risk: Naver API credentials could be exposed through configuration, chats, logs, or source control.

Mitigation: Store keys only in the intended secret configuration; do not paste or commit them, and rotate exposed keys.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/isnow890/skills/naver-search-mcp)
- [Naver Search MCP homepage](https://github.com/isnow890/naver-search-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown search summaries and trend analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, dates, prices, locations, and categories when relevant.]

## Skill Version(s):

1.0.54 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
