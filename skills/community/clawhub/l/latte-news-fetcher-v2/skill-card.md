## Description:

Fetches current news from free and public sources, supports RSS-oriented news discovery, and can use Tavily search to find alternative coverage.

This skill is for research and development only.

## Publisher:

[luogao2333](https://clawhub.ai/user/luogao2333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather today's news from selected public sources, fetch article details, and find alternative reporting when an original source is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct fetching can request arbitrary URLs without destination safeguards.

Mitigation: Restrict fetching to trusted public news domains or add URL validation that blocks localhost, private IP ranges, metadata endpoints, unsafe schemes, and redirects to internal hosts.

Risk: Search terms may be sent to Tavily when the optional API key is configured.

Mitigation: Avoid sensitive search queries and configure TAVILY_API_KEY only when third-party search disclosure is acceptable.

Risk: Fetched article and webpage text is untrusted content.

Mitigation: Treat fetched content as untrusted and verify important claims against trusted sources before acting on them.

Risk: The skill may persist news preferences in the workspace.

Mitigation: Review the preference-file behavior or disable persistence if local preference storage is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luogao2333/skills/latte-news-fetcher-v2)
- [Free News Sources and RSS](references/free-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news digest with links and concise summaries, plus optional plain-text command output from the news-fetch helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TAVILY_API_KEY for alternative source search and may persist workspace news preferences.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
