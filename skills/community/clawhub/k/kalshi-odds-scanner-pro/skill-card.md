## Description: <br>
Kalshi Odds Scanner Pro scans live sportsbook and Kalshi market prices to identify sports-market edge plays and can optionally place Kelly-sized Kalshi orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to set up and run a Python scanner that compares sportsbook-implied probabilities with Kalshi sports markets. It supports scan-only review and optional live order execution when the operator explicitly enables buying. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can place live real-money Kalshi orders when run with the buy option. <br>
Mitigation: Run in scan-only mode first, require an explicit confirmation step before live execution, and set per-run spend limits. <br>
Risk: The artifact includes hardcoded-looking API credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed keys, and configure credentials through local secrets or environment-specific files. <br>
Risk: Trading recommendations may be wrong or stale because they depend on external odds and market APIs. <br>
Mitigation: Review each proposed trade against current market data and account constraints before placing orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/themsquared/kalshi-odds-scanner-pro) <br>
- [The Odds API](https://the-odds-api.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external sportsbook and Kalshi APIs and may place live orders only when invoked with the buy option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
