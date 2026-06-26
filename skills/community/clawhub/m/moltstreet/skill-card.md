## Description: <br>
MoltStreet helps agents retrieve AI market signals, multi-analyst research, prediction accuracy, and paper-trading context for stocks, ETFs, and crypto through a public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredxyt](https://clawhub.ai/user/fredxyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch and summarize MoltStreet market outlooks, ticker-level analyst perspectives, actionable signals, consensus, prediction statistics, and paper-trade context. It is intended as market research support, not personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and market-search terms are sent to MoltStreet's public API. <br>
Mitigation: Use the skill only when sharing those query terms with MoltStreet is acceptable. <br>
Risk: AI-generated signals, analyst summaries, and paper-trade data may be incomplete, stale, or misleading if treated as investment advice. <br>
Mitigation: Treat outputs as research inputs, verify important claims independently, and avoid relying on the skill for personalized financial decisions. <br>
Risk: The skill depends on the availability and freshness of MoltStreet API responses. <br>
Mitigation: Check response freshness and API health before using the results in time-sensitive market analysis. <br>


## Reference(s): <br>
- [MoltStreet ClawHub Release](https://clawhub.ai/fredxyt/moltstreet) <br>
- [MoltStreet Homepage](https://moltstreet.com) <br>
- [MoltStreet Skill Documentation](https://moltstreet.com/skill.md) <br>
- [MoltStreet API Base](https://moltstreet.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or concise text synthesized from public API responses, with curl examples and JSON-backed market data when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No authentication required; depends on curl and availability of the MoltStreet public API.] <br>

## Skill Version(s): <br>
1.8.2 (source: server release, manifest.json, skill.json; artifact/_meta.json reports 1.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
