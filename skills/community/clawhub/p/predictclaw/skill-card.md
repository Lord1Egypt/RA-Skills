## Description:

Predict.fun skill with a PolyClaw-style CLI for markets, wallet funding, trading, positions, and hedging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walioo](https://clawhub.ai/user/walioo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to browse Predict.fun markets, inspect wallet readiness, manage funding and withdrawals, place trades, view positions, and scan hedge opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and trading workflows may handle real funds.

Mitigation: Start in fixture or read-only mode, review wallet and vault flows before live use, and keep limited funds on automation keys.

Risk: Custom API endpoints can change where market and trading requests are sent.

Mitigation: Avoid custom PREDICT_API_BASE_URL values unless the endpoint is fully trusted.

Risk: The mandated MCP command can execute a local subprocess in vault-related flows.

Mitigation: Set ERC_MANDATED_MCP_COMMAND only to a trusted executable and review vault risks before installation.

Risk: Security-sensitive dependencies and documentation conflicts may affect operational confidence.

Mitigation: Prefer releases with pinned security-sensitive dependencies and resolved README conflicts.

## Reference(s):

- [Predict.fun](https://predict.fun)
- [Predict.fun API](https://api.predict.fun)
- [ClawHub skill page](https://clawhub.ai/walioo/skills/predictclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mode-specific wallet, market, trading, position, and hedge guidance based on configured environment variables.]

## Skill Version(s):

0.1.34 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
