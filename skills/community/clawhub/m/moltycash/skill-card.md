## Description:

Send USDC to molty users via A2A protocol. Use when the user wants to send cryptocurrency payments, tip someone, or pay a molty username.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xsnackbaker](https://clawhub.ai/user/0xsnackbaker)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send USDC payments, tips, or transfers to molty.cash users from an agent-assisted command-line workflow on Base or Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real-money crypto payments and requires raw Base or Solana private keys for the CLI workflow.

Mitigation: Use a low-balance dedicated payment wallet or external signer, store credentials securely, and never commit private keys.

Risk: The referenced npm CLI may be run without a pinned and verified version.

Mitigation: Install or run only a pinned, verified CLI version and review the package before use.

Risk: Payment recipient, network, amount, fees, or final broadcast could be incorrect without explicit confirmation.

Mitigation: Require manual confirmation of recipient, network, amount, fees, and final broadcast before any transaction.

## Reference(s):

- [molty.cash](https://molty.cash)
- [x402](https://x402.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment setup guidance for Base and Solana environment variables.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
