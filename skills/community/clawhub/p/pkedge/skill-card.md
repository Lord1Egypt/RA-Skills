## Description: <br>
Monitors Polymarket prediction markets for pricing anomalies, evidence gaps, top-trader positioning, and fresh-wallet activity across SCAN, DEEP DIVE, WHALE WATCH, and INSIDER WATCH modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franks33](https://clawhub.ai/user/franks33) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-intelligence operators use this skill to generate Polymarket scans, single-market evidence reviews, whale-position reports, and fresh-wallet alerts for informational monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the release references persistent Telegram-posting automation but only ships instructions, not the runnable Node files. <br>
Mitigation: Inspect the referenced Node files and dependencies before installation, and do not run cron or launchd jobs until the code is available and reviewed. <br>
Risk: Telegram bot tokens and chat IDs can send messages to external channels if misconfigured or exposed. <br>
Mitigation: Use dedicated low-privilege Telegram bots, keep tokens out of source control, confirm destination chats, and require explicit pkedge-prefixed commands for external sends. <br>
Risk: Market, whale, and fresh-wallet signals can be incomplete, circumstantial, or misleading. <br>
Mitigation: Keep outputs framed as intelligence only, preserve the Not financial advice disclaimer, and avoid trading recommendations or accusations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/franks33/pkedge) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket Gamma markets endpoint](https://gamma-api.polymarket.com/markets?active=true&limit=200) <br>
- [Polymarket CLOB order book endpoint](https://clob.polymarket.com/book?token_id={tokenId}) <br>
- [Polymarket leaderboard endpoint](https://data-api.polymarket.com/v1/leaderboard?timePeriod=ALL&orderBy=PNL&limit=50) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and Telegram-ready alert text with inline shell commands for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scheduled market scans, single-market analysis, and alert summaries; appends a financial-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
