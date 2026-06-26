## Description: <br>
Tracks Kalshi event contract prices, order book depth, recent trades, and American-odds conversions across prediction-market categories without executing trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Kalshi prediction-market events, prices, liquidity, recent trades, and odds conversions for sports, politics, economics, weather, finance, and entertainment markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Kalshi API key for authenticated market-data requests. <br>
Mitigation: Use a dedicated or least-privilege API key if available and keep the key out of chat transcripts, logs, and committed files. <br>
Risk: Future edits could expand the skill beyond read-only market-data operations. <br>
Mitigation: Review future versions for order-placement or account-management endpoints before installation or execution. <br>
Risk: Market prices, order books, and recent trades can be stale, thin, or volatile. <br>
Mitigation: Report volume, open interest, close time, top-of-book depth, and bid/ask spread so users can judge liquidity and timing. <br>


## Reference(s): <br>
- [Kalshi](https://kalshi.com/) <br>
- [Kalshi Tracker Tutorial](https://agentbets.ai/guides/openclaw-kalshi-tracker-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/kalshi-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and KALSHI_API_KEY for authenticated read-only Kalshi API requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
