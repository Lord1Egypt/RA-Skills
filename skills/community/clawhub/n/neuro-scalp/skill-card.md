## Description:

Neuro Scalp provides an AI-driven OKX cryptocurrency scalping bot with market data ingestion, reinforcement-learning signals, risk controls, order execution, backtesting, walk-forward testing, and a FastAPI monitoring dashboard.

This skill is for research and development only.

## Publisher:

[shayuqiang671-rgb](https://clawhub.ai/user/shayuqiang671-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and trading-system reviewers use this skill to evaluate or adapt a prototype automated crypto scalping system for OKX, including testnet validation, backtesting, walk-forward testing, and dashboard monitoring. It should not be connected to funded accounts until live trading gates, private infrastructure, trusted model checkpoints, and enforced risk limits are in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot can place live OKX orders if configured with real credentials.

Mitigation: Use isolated paper or testnet credentials with withdrawals disabled, and add an explicit live-trading gate before any funded-account use.

Risk: Risk controls are incomplete or inconsistently applied across configuration and execution code.

Mitigation: Enforce max drawdown, position size, leverage, slippage, kill switch, and exchange-side limits before allowing live order placement.

Risk: Redis and the FastAPI dashboard may expose trading data or controls if reachable from untrusted networks.

Mitigation: Bind Redis and the dashboard to private networks, add authentication, and place the dashboard behind controlled access.

Risk: Model checkpoints and dependencies can alter trading behavior or introduce supply-chain risk.

Mitigation: Load checkpoints only from trusted verified sources, pin and update dependencies, and scan the environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shayuqiang671-rgb/skills/neuro-scalp)
- [ClawHub publisher profile](https://clawhub.ai/user/shayuqiang671-rgb)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and project files with Python, YAML, HTML, Docker Compose, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance and runnable project artifacts for research, testnet validation, backtesting, walk-forward testing, and monitoring.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
