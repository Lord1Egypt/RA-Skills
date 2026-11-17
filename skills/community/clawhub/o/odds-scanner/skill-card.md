## Description:

Fetch live sports betting odds from 20+ sportsbooks and compare lines for NFL, NBA, MLB, NHL, soccer, and other sports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current sports odds, compare sportsbook lines, identify best available lines, and inspect vig or hold percentage for betting markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ODDS_API_KEY to api.the-odds-api.com when API commands are run.

Mitigation: Use a dedicated API key, avoid shell tracing or command logging that could expose it, rotate the key if exposure is suspected, and apply provider-side quotas or permission limits where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/skills/odds-scanner)
- [The Odds API](https://the-odds-api.com/)
- [AgentBets OpenClaw Odds Scanner guide](https://agentbets.ai/guides/openclaw-odds-scanner-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Analysis, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and an ODDS_API_KEY credential for The Odds API.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
