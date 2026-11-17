## Description:

Connect wallets via WalletConnect v2 and execute EVM signing and contract-call operations on Ethereum and BSC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawson-ccy](https://clawhub.ai/user/lawson-ccy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pair an EVM wallet, request wallet authentication or signatures, inspect saved sessions, and submit Ethereum or BSC contract calls through WalletConnect. It is suited to agent workflows that need wallet-mediated approval before signing or sending transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an agent-accessible wallet bridge that can request signatures and send EVM transactions.

Mitigation: Use a dedicated wallet with limited funds and allowances, review every wallet prompt, and require explicit user confirmation before signing or sending.

Risk: WalletConnect session data and debug logs can contain sensitive wallet or session information.

Mitigation: Treat ~/.agent-wallet contents and debug logs as sensitive, restrict access to them, and enable debug logging only when needed for troubleshooting.

Risk: The --open pairing option invokes a system file opener for the QR image.

Mitigation: Avoid --open until shell execution is fixed; prefer QR image delivery through the agent channel and use the WalletConnect URI only as a fallback.

Risk: Transaction simulation can be bypassed with --no-simulate.

Mitigation: Keep simulation enabled by default and bypass it only after the user explicitly accepts the added transaction risk.

Risk: The artifact includes a default WalletConnect project ID.

Mitigation: Prefer an operator-controlled WalletConnect project ID through WALLETCONNECT_PROJECT_ID for production use.

## Reference(s):

- [Lista Wallet Connect on ClawHub](https://clawhub.ai/lawson-ccy/skills/lista-wallet-connect)
- [Supported Chains & Tokens](references/chains.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON status payloads for agent parsing, with concise text or Markdown summaries for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet-request commands can emit interim approval events before a terminal status, and pairing may produce QR image paths or WalletConnect URI fallbacks.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
