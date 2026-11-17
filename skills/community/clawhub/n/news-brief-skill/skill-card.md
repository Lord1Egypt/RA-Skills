## Description:

Creates personalized news briefs from configured interests, summarizes matching stories, delivers them through user-selected channels, and supports feedback-driven adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17oko](https://clawhub.ai/user/17oko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect news from configured APIs, RSS feeds, and crawlers, then receive concise topic-focused briefs through channels such as chat, email, DingTalk, or Telegram. Developers may also adapt the configuration and scripts to add sources, delivery channels, or summarization behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User IDs and backup paths can affect local file locations used for configuration, logs, and recovery data.

Mitigation: Validate and normalize user_id values before filesystem use, isolate each user directory, and enforce bounded backup retention before multi-user deployment.

Risk: The skill sends requests to news sources and delivery endpoints, including user-configured webhooks and messaging APIs.

Mitigation: Run with restricted outbound network access and allowlist only intended news and delivery providers.

Risk: SMTP, bot, and webhook credentials may be stored for delivery integrations.

Mitigation: Use a contained non-privileged account, avoid high-value credentials, and improve secret storage before production use.

## Reference(s):

- [News Brief Skill Detailed Documentation](references/documentation.md)
- [ClawHub Skill Page](https://clawhub.ai/17oko/skills/news-brief-skill)
- [Publisher Profile](https://clawhub.ai/user/17oko)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown-style news brief text with configuration guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source labels, credibility notes, delivery status, feedback prompts, and preview briefs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
