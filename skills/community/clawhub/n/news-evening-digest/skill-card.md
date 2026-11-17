## Description:

Each evening at 20:00, this skill fetches global news, generates a structured digest, and posts it to configured messaging channels using sources such as World Monitor and Tavily Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to schedule automated evening news digests for operational awareness. It gathers current news, formats a concise digest, and sends notifications after local webhook and scheduling configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation can post to a WeCom webhook that is not described consistently in the documentation and may notify everyone in the destination channel.

Mitigation: Verify WECOM_WEBHOOK_URL before running the script, remove the default @all notification unless explicitly intended, and align the documented delivery channels with the implementation.

Risk: Webhook URLs and search API keys are operational secrets used by the scheduled script.

Mitigation: Store webhook URLs and API keys only in local environment configuration, rotate them if exposed, and avoid committing real values into skill files.

Risk: Automated news aggregation may send incomplete or inaccurate summaries to external channels.

Mitigation: Review the configured sources and digest output before production use, especially for high-impact geopolitical, financial, or emergency topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/news-evening-digest)
- [ClawHub publisher profile](https://clawhub.ai/user/cp3d1455926-svg)
- [World Monitor API](https://api.worldmonitor.app)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scheduled digest message intended for delivery through configured notification channels.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
