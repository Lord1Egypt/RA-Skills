## Description:

Tracks Kalshi event contract prices, order book depth, recent trades, and American odds conversions across sports, politics, economics, weather, finance, and entertainment markets without executing trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to query Kalshi prediction markets, inspect prices, liquidity, and recent trades, and compare contract prices with sportsbook-style American odds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent needs access to a Kalshi API key for read-only market queries.

Mitigation: Use a scoped or revocable key if Kalshi supports it, and rotate or revoke the key when access is no longer needed.

Risk: The skill runs commands that contact Kalshi's API with the configured credential.

Mitigation: Review generated commands before running them and keep the key out of shared logs, transcripts, and committed files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/kalshi-tracker)
- [Kalshi](https://kalshi.com/)
- [AgentBets Kalshi Tracker Guide](https://agentbets.ai/guides/openclaw-kalshi-tracker-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-shaped API summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and KALSHI_API_KEY; performs read-only Kalshi API queries.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
