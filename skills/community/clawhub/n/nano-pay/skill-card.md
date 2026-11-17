## Description:

Pay for x402-priced HTTP APIs (HTTP 402 Payment Required) with feeless, sub-second Nano (XNO) micropayments from a self-custodied local wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glennquinting](https://clawhub.ai/user/glennquinting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to quote and pay x402 HTTP 402 APIs with Nano micropayments, manage a local low-balance wallet, top up funds, and optionally serve paid agent endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install unpinned payment software and operate persistent wallets that can move real funds.

Mitigation: Verify the feeless402 package and version before installation, use an isolated environment, and keep only a low working balance in the wallet.

Risk: Payment, send, top-up execution, and server actions can transfer or expose funds and may be irreversible.

Mitigation: Require explicit approval before pay, send, topup --execute, or serve actions, and quote or check balances before moving funds.

Risk: Wallet secrets may be exposed if the local wallet file or unrelated environment variables are shared with tools or logs.

Mitigation: Do not print, commit, paste, or transmit wallet seeds, and avoid exposing unrelated environment variables to the runtime.

## Reference(s):

- [ClawHub nano-pay Skill](https://clawhub.ai/glennquinting/skills/nano-pay)
- [Feeless402 Homepage](https://feeless402.com)
- [x402nano](https://www.x402nano.org/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides installation of the feeless402 CLI and actions that create wallets, quote prices, move Nano funds, top up through NanSwap, or serve paid endpoints.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
