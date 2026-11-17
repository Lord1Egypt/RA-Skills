## Description:

German-language news skill that helps OpenClaw and AI agents fetch ClawNews.de briefings, archive search results, and breaking alerts about OpenClaw, ClawHub, LLMs, AI agents, security, tools, open source, and community topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawnewsde](https://clawhub.ai/user/clawnewsde)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users in the DACH region use this skill to receive German-language briefings, search the ClawNews.de archive, and surface breaking alerts about the AI agent ecosystem.

### Deployment Geography for Use:

DACH region

## Known Risks and Mitigations:

Risk: Breaking alerts remain active in every mode.

Mitigation: Install only when always-on breaking alerts are acceptable for the intended agent and user workflow.

Risk: The skill can rely on persistent memory or proactive checks for monitoring.

Mitigation: Avoid enabling scheduler, heartbeat, or persistent-memory behavior unless background news monitoring is intended.

Risk: The skill uses ClawNews.de as a fixed news source.

Mitigation: Treat results as source-specific news summaries and verify important items with additional sources before acting on them.

## Reference(s):

- [claw://News ClawHub listing](https://clawhub.ai/clawnewsde/skills/newsticker)
- [clawnewsde publisher profile](https://clawhub.ai/user/clawnewsde)
- [ClawNews.de](https://clawnews.de)
- [ClawNews.de RSS feed](https://clawnews.de/feed/)
- [ClawNews.de breaking feed](https://clawnews.de/category/breaking/feed/)
- [ClawNews.de WordPress categories API](https://clawnews.de/wp-json/wp/v2/categories)
- [claw://News formatting templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [German-language Markdown with links and short structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include briefings, archive search summaries, breaking alerts, setup prompts, and settings summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
