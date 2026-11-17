## Description:

MPC-secured crypto wallet via Portal for checking balances, sending tokens, signing transactions, and swapping tokens across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rshahatit](https://clawhub.ai/user/rshahatit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent controlled access to a Portal MPC wallet for balances, token transfers, transaction signing, token swaps, and wallet setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move cryptocurrency funds and sign data from an agent-controlled wallet.

Mitigation: Use only test wallets or negligible balances unless a fail-closed Portal signature approval webhook enforces spending limits, recipient allowlists, chain restrictions, and raw-signature denial.

Risk: The Portal client API key and MPC signing shares may be stored together in local configuration.

Mitigation: Prefer a keychain, secret manager, or separated credential store for production credentials, and keep credential-bearing configuration out of version control.

Risk: Prompt injection or ambiguous signing requests could lead to unintended approvals, permits, transfers, or raw signatures.

Mitigation: Require explicit user confirmation, double-confirm larger transfers, simulate or evaluate transactions before signing, decode typed or personal-sign messages, and refuse requests that bypass safety checks.

## Reference(s):

- [Portal Wallet on ClawHub](https://clawhub.ai/rshahatit/skills/portal-wallet)
- [Portal OpenClaw Skill homepage](https://github.com/portal-hq/portal-openclaw-skill)
- [Portal documentation](https://docs.portalhq.io)
- [Portal signature approval webhooks](https://docs.portalhq.io/resources/alert-webhooks#signature-approvals)
- [Portal dashboard](https://app.portalhq.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and jq shell command examples and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, PORTAL_CLIENT_API_KEY, PORTAL_SECP256K1_SHARE, and PORTAL_ED25519_SHARE.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
