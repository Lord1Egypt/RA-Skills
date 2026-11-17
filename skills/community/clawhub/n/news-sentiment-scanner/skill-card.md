## Description:

Scan news sources and RSS feeds for events that could move prediction market prices. Score headlines for market impact, flag urgent stories, and cross-reference with active markets. Use when asked about breaking news, market-moving events, or news sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to scan current public RSS headlines for market-moving events, news sentiment, urgent stories, and prediction-market trading signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests to public news and RSS providers.

Mitigation: Install only when network access to those public providers is acceptable for the agent environment.

Risk: Fetched headlines are untrusted external context and may be incomplete, stale, or misleading.

Mitigation: Verify important claims before making prediction-market or trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/skills/news-sentiment-scanner)
- [AgentBets OpenClaw News Sentiment Scanner guide](https://agentbets.ai/guides/openclaw-news-sentiment-scanner-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and headline analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and python3; fetches public RSS headlines and parses them locally.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
