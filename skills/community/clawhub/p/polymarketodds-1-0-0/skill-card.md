## Description: <br>
Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum. Includes watchlist alerts, resolution calendar, momentum scanner, and paper trading (simulated, no real money). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsjustFred](https://clawhub.ai/user/itsjustFred) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket odds, monitor market movement, manage local watchlists, and simulate paper trades without connecting a wallet or executing real transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records watched markets and simulated paper trades under ~/.polymarket. <br>
Mitigation: Review or remove the local watchlist and portfolio JSON files when they are no longer needed. <br>
Risk: Cron-based alerts or digests can continue running after setup. <br>
Mitigation: Track any cron entries created for this skill and remove them when alerts or digests are no longer wanted. <br>
Risk: Market odds and simulated portfolio values are informational and depend on public Polymarket API responses. <br>
Mitigation: Verify market details directly with Polymarket before relying on the information for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/itsjustFred/polymarketodds-1-0-0) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style terminal text with inline command examples and local JSON records for watchlists and paper portfolios] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the requests package; reads public Polymarket data and can store optional local files under ~/.polymarket.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
