## Description: <br>
帮助使用者在 Cursor 中编写聚宽（JoinQuant）量化策略，提供策略模板、代码片段、API 参考和风险管理示例。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daidaotian](https://clawhub.ai/user/daidaotian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative strategy authors use this skill to draft JoinQuant strategy templates, look up common data and order APIs, and adapt reusable snippets for backtesting or platform-specific strategy development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-pastable examples may place orders, cancel orders, rebalance portfolios, or liquidate holdings when adapted or run in a live JoinQuant environment. <br>
Mitigation: Backtest or paper trade first, add account-mode checks, position limits, and explicit confirmation gates before live deployment. <br>
Risk: Strategy templates and snippets are reference material and may need adjustment for a user's portfolio, market assumptions, and platform rules. <br>
Mitigation: Review the generated strategy logic, validate it against JoinQuant platform requirements, and tune risk controls before using real capital. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daidaotian/joinquant-strategy) <br>
- [README](artifact/README.md) <br>
- [Core API reference](artifact/api_reference/core_functions.md) <br>
- [Data API reference](artifact/api_reference/data_functions.md) <br>
- [Order API reference](artifact/api_reference/order_functions.md) <br>
- [Risk control snippets](artifact/snippets/risk_control.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python strategy templates and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include JoinQuant order, cancellation, rebalancing, liquidation, and risk-control code that should be reviewed before live use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
