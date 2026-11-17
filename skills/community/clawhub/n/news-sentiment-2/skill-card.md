## Description:

Scans Hong Kong, U.S., and A-share company announcements, news, analyst research, and social media to denoise signals, score sentiment from -10 to +10, and produce a sentiment thermometer with major-event summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent operators use this skill to monitor market news and social sentiment for listed companies across Hong Kong, U.S., and A-share markets. It produces sentiment scores, weighted source summaries, major-event lists, and caveats for market monitoring and decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests or normalizes broad agent powers, including command execution, file writes, callback URLs, and external API or network access without clear scope.

Mitigation: Use it only in a controlled workspace, require explicit approval for command execution and file writes, restrict network access, and do not allow callbacks to untrusted URLs.

Risk: Sensitive prompts, API keys, or workspace data could be exposed through external services, logs, callbacks, or command output.

Mitigation: Use least-privilege or disposable credentials, avoid sensitive prompts and data, keep secrets out of logs and version control, and review outbound requests before execution.

Risk: Market sentiment outputs can be incomplete, stale, manipulated, or inaccurate, especially for social media sources or thinly discussed securities.

Mitigation: Treat outputs as informational only, cross-check material events against official disclosures and high-weight sources, and do not use the skill as standalone investment advice.

## Reference(s):

- [ClawHub skill release: news-sentiment-2](https://clawhub.ai/thcjp/skills/news-sentiment-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style sentiment report with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sentiment scores range from -10 to +10 and may include weighted sources, major events, confidence values, statistics, operational suggestions, and limitations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
