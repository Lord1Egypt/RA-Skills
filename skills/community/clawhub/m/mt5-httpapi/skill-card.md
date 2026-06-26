## Description: <br>
HTTP client for a user-deployed mt5-httpapi MetaTrader 5 bridge that can read account, market, history, technical-analysis, order, position, terminal, and backtest endpoints when MT5_API_URL is explicitly configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation operators use this skill to interact with an already deployed mt5-httpapi bridge for account inspection, market data, server-side technical analysis, order and position management, terminal operations, and MT5 backtest workflows. The skill is appropriate only when the user has explicitly provided MT5_API_URL and any required MT5_API_TOKEN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trade-mutating endpoints can affect a real brokerage account. <br>
Mitigation: Require explicit confirmation for each mutating order, position, terminal restart, or terminal shutdown action after showing the resolved broker URL, account, symbol, side, volume, price, SL, and TP. <br>
Risk: A missing or weak API token can expose account state and trading actions to any process that can reach the server. <br>
Mitigation: Use MT5_API_TOKEN only from the user-provided environment or direct user input, require a strong server api_token before non-local exposure, and avoid reading credentials from repository config files. <br>
Risk: Backtests can run against the wrong terminal or wrong account path. <br>
Mitigation: Verify the MT5_API_URL broker/account prefix, check the target terminal mode with /ping, and report exact endpoint, HTTP status, and response body on failures. <br>
Risk: The security evidence flags powerful maintainer workflows that should be run deliberately around sensitive repositories or credentials. <br>
Mitigation: Follow the documented confirmation steps and use lower-access modes such as --no-yolo or fallback-reviewer none when appropriate. <br>


## Reference(s): <br>
- [mt5-httpapi setup](references/setup.md) <br>
- [mt5-httpapi repository](https://github.com/psyb0t/mt5-httpapi) <br>
- [wickworks technical analysis sidecar](https://github.com/psyb0t/docker-wickworks) <br>
- [wickworks indicator catalog](https://github.com/psyb0t/docker-wickworks#available-indicators) <br>
- [ClawHub skill page](https://clawhub.ai/psyb0t/mt5-httpapi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, curl examples, JSON request and response examples, and file paths for generated backtest artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided MT5_API_URL and, when server auth is enabled, MT5_API_TOKEN; mutating trade and terminal actions require explicit per-action user confirmation.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
