## Description: <br>
Trade prediction markets on Kalshi using the kalshi-cli command-line tool for market discovery, order placement, portfolio management, live price streaming, and terminal charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lacymorrow](https://clawhub.ai/user/lacymorrow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to operate the kalshi-cli tool for Kalshi prediction-market research, order entry, portfolio checks, streaming market data, and bot-oriented command workflows. It is informational tooling for user-directed trading, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production mode can place or cancel real-money Kalshi orders. <br>
Mitigation: Start in demo mode and require explicit user review of market, side, quantity, price, --prod, --yes, and cancel-all details before execution. <br>
Risk: The skill depends on an external kalshi-cli installation with access to a Kalshi account. <br>
Mitigation: Install only from a trusted kalshi-cli source, confirm authentication status, and avoid exposing API keys or private keys in prompts, logs, or shared files. <br>
Risk: Trading event contracts can result in financial loss and the skill is not a financial advisor. <br>
Mitigation: Provide tool usage and command construction only; leave trading decisions to the user and encourage demo-mode testing before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lacymorrow/kalshi-cli-trading) <br>
- [kalshi-cli](https://github.com/6missedcalls/kalshi-cli) <br>
- [OpenClaw Kalshi Trading Skill](https://github.com/lacymorrow/openclaw-kalshi-trading-skill) <br>
- [Kalshi API Docs](https://docs.kalshi.com/welcome) <br>
- [Kalshi Fee Schedule](https://kalshi.com/fee-schedule) <br>
- [Liquidity Incentive Program](https://help.kalshi.com/incentive-programs/liquidity-incentive-program) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading command proposals that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
