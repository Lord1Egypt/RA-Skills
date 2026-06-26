## Description: <br>
Query Polymarket prediction markets - check odds, trending markets, search events, track prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leochan14](https://clawhub.ai/user/leochan14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up public Polymarket prediction market data, including trending markets, keyword searches, event details, categories, odds, volume, and end dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and request parameters are sent to Polymarket's public API. <br>
Mitigation: Avoid entering private, sensitive, or embargoed research topics when querying markets. <br>
Risk: The helper script depends on the Python requests package and external Polymarket API availability. <br>
Mitigation: Install dependencies from trusted sources and treat API errors or stale market data as lookup failures rather than authoritative investment guidance. <br>
Risk: The skill provides market information but does not implement trading, wallets, or authentication. <br>
Mitigation: Use it for read-only research only and perform any trading-related actions outside this skill with separate review. <br>


## Reference(s): <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket Documentation](https://docs.polymarket.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/leochan14/polymarket-1-0-0) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/leochan14) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown-formatted command output with market summaries and optional raw JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market lookup; normal operation sends query terms and request parameters to Polymarket's public API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
