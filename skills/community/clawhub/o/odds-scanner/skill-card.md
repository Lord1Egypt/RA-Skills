## Description: <br>
Fetch live sports betting odds from 20+ sportsbooks and compare lines for NFL, NBA, MLB, NHL, soccer, and other supported sports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch current sports betting odds, compare sportsbook lines, and identify best available spreads, totals, or prices using The Odds API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a The Odds API key and sends requested sports, markets, and lookup parameters to a third-party odds service. <br>
Mitigation: Use a dedicated API key, avoid sharing unnecessary sensitive context in odds requests, and monitor API quota or billing. <br>
Risk: Live sportsbook odds can change quickly and may be incomplete or unavailable for some sports or markets. <br>
Mitigation: Treat returned odds as time-sensitive, verify important lines with the sportsbook or data provider, and disclose the retrieval time when using results. <br>


## Reference(s): <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [The Odds API active sports endpoint](https://api.the-odds-api.com/v4/sports?apiKey=$ODDS_API_KEY) <br>
- [AgentBets OpenClaw odds scanner guide](https://agentbets.ai/guides/openclaw-odds-scanner-skill/) <br>
- [AgentBets OpenClaw skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API-response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an ODDS_API_KEY credential for The Odds API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
