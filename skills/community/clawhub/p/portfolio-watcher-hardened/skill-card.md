## Description: <br>
Monitor stock/crypto holdings, get price alerts, track portfolio performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track manually supplied stock, ETF, and crypto holdings, check prices, set alerts, and review approximate portfolio performance without connecting a brokerage account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The finance helper activates on broad price-related phrases and may handle sensitive portfolio information in unintended contexts. <br>
Mitigation: Install only if broad portfolio and price triggers are acceptable, and require explicit confirmation before revealing holdings or creating alerts in shared contexts. <br>
Risk: Delayed or stale market data could be mistaken for exact figures for trading, tax, or other financial decisions. <br>
Mitigation: Label computed gains, losses, P&L, and performance values as approximate, state data freshness limits, and avoid presenting the output as financial advice. <br>
Risk: Portfolio holdings, values, positions, and performance are sensitive financial data. <br>
Mitigation: Do not display portfolio data in public channels, group chats, or shared workspaces unless the user explicitly confirms disclosure. <br>
Risk: Destructive changes such as deleting holdings, resetting portfolios, or clearing alerts can cause user data loss. <br>
Mitigation: Require fresh, explicit confirmation before each destructive portfolio or alert change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/portfolio-watcher-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/portfolio-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational responses with portfolio summaries, price-alert guidance, and safety caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial figures should be labeled approximate and accompanied by data freshness limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
