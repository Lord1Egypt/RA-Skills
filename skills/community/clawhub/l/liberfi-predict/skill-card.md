## Description:

Browse and trade prediction markets by listing events, viewing event details and embedded markets, checking Kalshi and Polymarket USDC balances, viewing positions and trade history, inspecting orders, and placing or canceling orders through the LiberFi CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse prediction-market events, review balances and positions, and prepare prediction-market orders on Kalshi and Polymarket. It supports real trading workflows, so order placement and cancellation require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel real prediction-market orders and can deploy a Safe or approve tokens.

Mitigation: Require an explicit user confirmation after a plain-language order or setup summary before executing any trade, cancellation, setup, or approval action.

Risk: The skill can query private financial data through managed wallet addresses.

Mitigation: Use the authenticated user flow only when the user asks for their own prediction-market data, and summarize balances, positions, and trades without exposing wallet details unless requested.

Risk: The skill may install a global LiberFi CLI package automatically.

Mitigation: Review the package source and installation path before deployment, and run the skill in an environment where global package installation is acceptable.

Risk: Incorrect Polymarket address handling can produce empty balances or direct users to the wrong funding path.

Mitigation: For balance, positions, and trades, pass the TEE EOA returned by whoami; use the Safe address only to fetch bridge deposit addresses.

## Reference(s):

- [Predict TEE Order Flow](reference/order-flow.md)
- [LiberFi homepage](https://liberfi.io)
- [ClawHub skill page](https://clawhub.ai/bombmod/skills/liberfi-predict)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured --json CLI output and requires explicit confirmation before executing trades or cancellations.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
