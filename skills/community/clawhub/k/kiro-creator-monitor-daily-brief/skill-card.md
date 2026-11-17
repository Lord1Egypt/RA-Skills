## Description:

Monitor creator topics across X, RSS, GitHub, and Reddit; deduplicate and score results; produce a daily top-5 brief plus one publish-ready X/LinkedIn draft; optional scheduled delivery to Telegram, Slack, or email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmining](https://clawhub.ai/user/vmining)

### License/Terms of Use:


## Use Case:

External creators, founders, and marketing or developer-relations teams use this skill to monitor AI/Web3 topics, rank fresh items, and produce a daily brief plus ready-to-edit X and LinkedIn posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to configured public sources and may be affected by custom feed URLs or service rate limits.

Mitigation: Review configured source URLs before use and keep the configuration writable only by trusted users.

Risk: Optional delivery can send the full generated brief to third-party messaging or email services using supplied credentials.

Mitigation: Enable Telegram, Slack, or email delivery only for approved destinations and protect delivery credentials as secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmining/skills/kiro-creator-monitor-daily-brief)
- [Kiro homepage](https://kiroai.io)
- [OpenAI News RSS feed](https://openai.com/news/rss.xml)
- [The Verge AI RSS feed](https://www.theverge.com/rss/ai-artificial-intelligence/index.xml)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown daily brief, JSON result payload, and concise command/status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes latest.md and latest.json to the configured output directory; optional delivery can send the full generated brief to Telegram, Slack, or email.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
