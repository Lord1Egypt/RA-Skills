## Description: <br>
Query Polymarket prediction markets. Check odds, find trending markets, search events, track price movements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xvolica](https://clawhub.ai/user/xvolica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect public Polymarket market data, monitor watched markets, review price movements, and maintain a local paper-trading portfolio without placing real trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watched markets and simulated trades are stored locally in ~/.polymarket. <br>
Mitigation: Review or remove the local JSON files when needed, especially on shared systems. <br>
Risk: Cron examples can create recurring background checks for alerts or digests. <br>
Mitigation: Add scheduled checks only intentionally and review the cron entries after setup. <br>
Risk: Market odds and paper-trading results may be mistaken for financial advice or real trading activity. <br>
Mitigation: Treat outputs as informational only; the skill does not perform wallet actions, blockchain transactions, or real trades. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xvolica/polymarket-trade-1-0-6) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>
- [Step-by-step guide](https://telegra.ph/How-Building-a-Weather-Polymarket-Bot-with-OpenClaw-Skill-and-turn-100--8000-Step-by-Step-Guide-02-28-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style CLI text with market summaries and local JSON watchlist and portfolio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads public Polymarket data over HTTPS and can store watchlists and simulated trades in ~/.polymarket.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports package version 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
