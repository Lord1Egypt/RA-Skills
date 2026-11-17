## Description:

Predict.fun skill with a PolyClaw-style CLI for markets, wallet funding, trading, positions, and hedging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walioo](https://clawhub.ai/user/walioo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use PredictClaw to browse predict.fun markets, check wallet readiness, manage deposits and withdrawals, place buy orders, inspect positions, and scan hedge opportunities. Signer-backed modes support live trading workflows and should be configured deliberately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports live trading and wallet-control workflows that can use sensitive keys and authenticated requests.

Mitigation: Use test-fixture or testnet first, keep only limited funds on automation keys, and review signer-backed commands before use.

Risk: Custom API base URLs can redirect authenticated requests to external targets.

Mitigation: Avoid custom PREDICT_API_BASE_URL values unless you control and trust the endpoint.

Risk: The mandated-vault mode can invoke an MCP executable in an environment that may contain secrets.

Mitigation: Only enable ERC_MANDATED_MCP_COMMAND for a trusted executable in a clean environment without unrelated secrets.

## Reference(s):

- [Predict.fun](https://predict.fun)
- [ClawHub skill page](https://clawhub.ai/walioo/skills/predictclaw-publish-docs-20260320)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that return JSON for wallet, market, trade, position, and hedge workflows.]

## Skill Version(s):

0.1.11 (source: release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
