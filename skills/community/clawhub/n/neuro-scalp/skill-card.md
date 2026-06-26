## Description: <br>
AI-driven high-frequency crypto scalping bot for OKX with reinforcement learning, dynamic risk control, and real-time market data monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shayuqiang671-rgb](https://clawhub.ai/user/shayuqiang671-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading teams use this skill to set up an automated OKX crypto scalping system with market data ingestion, model-driven signals, order execution, risk controls, backtesting, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates cryptocurrency trading paths that may place live OKX orders and create real-money loss exposure. <br>
Mitigation: Audit and modify the skill before use, confirm sandbox or testnet enforcement, and require an explicit live-trading opt-in before providing live OKX credentials. <br>
Risk: The available security summary says the live-order path is purpose-aligned but under-scoped for financial automation. <br>
Mitigation: Add strict order limits, drawdown limits, and kill-switch behavior, then validate the controls with backtests and testnet runs before live deployment. <br>
Risk: Backtest data path behavior and strategy controls may not be sufficient for production decisions without review. <br>
Mitigation: Validate data inputs, slippage assumptions, commissions, and walk-forward evaluation before relying on reported strategy performance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shayuqiang671-rgb/neuro-scalp) <br>
- [Publisher profile](https://clawhub.ai/user/shayuqiang671-rgb) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with Python project files, YAML configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading automation scaffolding, configuration, backtesting utilities, and dashboard components for agent-assisted setup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
