## Description:

Crypto trading: swap, perps, transfer, pay, deposit (credit card / crypto), withdraw, AI chat, market discovery, x402 payment, autopilot. Built-in wallet via Minara CLI. EVM + Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larisgtu](https://clawhub.ai/user/larisgtu)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to route crypto wallet, trading, deposit, withdrawal, market discovery, AI analysis, and x402 payment tasks through the Minara CLI. It is intended for workflows involving EVM and Solana assets, including high-impact actions that require explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable global Minara CLI and can control wallet, payment, and trading actions.

Mitigation: Use a pinned, reviewed CLI version in a dedicated environment before granting access to funds or trading accounts.

Risk: Fund-moving commands, perps, withdrawals, x402 payments, and autopilot can create financial loss if parameters are wrong or approvals are skipped.

Mitigation: Verify recipients, chains, token amounts, leverage, and trade direction independently, and keep explicit confirmation enabled for every transaction.

Risk: Minara API keys or logged-in CLI sessions can authorize sensitive wallet and trading operations.

Mitigation: Keep credentials narrowly scoped, avoid sharing them across environments, and remove or rotate credentials when access is no longer needed.

## Reference(s):

- [Minara homepage](https://minara.ai)
- [ClawHub skill page](https://clawhub.ai/larisgtu/skills/minara-skill-v2)
- [Coinbase x402 quickstart for buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fund-moving actions require explicit user confirmation; read-only CLI commands may return text or JSON when supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
