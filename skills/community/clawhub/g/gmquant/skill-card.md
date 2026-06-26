## Description: <br>
掘金量化 Python SDK expert skill for Chinese-language strategy development, market data queries, backtesting, live trading workflows, and gm.api reference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turkeydick](https://clawhub.ai/user/turkeydick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative traders use this skill to turn Chinese natural-language trading ideas into gm.api strategy code, market-data queries, and backtest or live-run commands for the 掘金量化 platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed API tokens. <br>
Mitigation: Rotate or ignore bundled tokens, use a personal token through environment variables or a secret manager, and avoid pasting secrets into chat. <br>
Risk: The security evidence reports under-scoped live-trading execution paths. <br>
Mitigation: Require explicit manual confirmation before using live mode, account IDs, order placement, close-all operations, or bond conversion examples. <br>
Risk: Generated or bundled trading strategies can cause financial loss if run without review. <br>
Mitigation: Review generated strategy logic, run backtests or simulation first, and verify orders and risk controls before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turkeydick/gmquant) <br>
- [掘金量化终端](https://www.myquant.cn) <br>
- [Quick Start and Strategy Architecture](references/01-quick-start.md) <br>
- [Core Functions](references/02-core-functions.md) <br>
- [Market Data Queries](references/04-market-data.md) <br>
- [Trading Order API](references/08-order-api.md) <br>
- [Account Query Functions](references/10-account-query.md) <br>
- [User Guide](references/15-user-guide.md) <br>
- [Premium Data API Summary](references/16-premium-data-apis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce runnable Python strategy files and commands that require a local gm SDK, a 掘金 terminal session, and user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
