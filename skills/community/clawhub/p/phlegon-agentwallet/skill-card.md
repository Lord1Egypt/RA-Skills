## Description:

AgentWallet is a secure multi-chain wallet skill for AI agents to create wallets, check balances, sign and broadcast transactions across EVM chains, Solana, and TON while keeping private keys in the vault process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phlegonlabs](https://clawhub.ai/user/phlegonlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentWallet to automate wallet creation, balance checks, transaction signing, transfers, x402 payment signing, and session-based wallet operations across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can sign or transfer assets with high-impact financial consequences.

Mitigation: Require explicit approval for each transaction and independently verify recipient, chain, token, and amount before signing or broadcasting.

Risk: Blind signing or opaque transaction payloads can authorize unintended actions.

Mitigation: Decode and review transaction intent before signing, and reject requests whose recipient, amount, network, or contract action cannot be verified.

Risk: Long-lived sessions or exposed tokens can extend wallet authority beyond the intended task.

Mitigation: Use short token lifetimes, keep credentials out of command arguments, and lock the wallet session immediately after use.

Risk: Installing an unpinned wallet CLI package can introduce supply-chain risk.

Mitigation: Use a pinned or verified package release and review the package before installing it in environments with real funds.

## Reference(s):

- [AgentWallet ClawHub skill page](https://clawhub.ai/phlegonlabs/skills/phlegon-agentwallet)
- [AgentWallet source repository (declared metadata)](https://github.com/user/agentwallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing CLI procedures and cautions; wallet commands can return JSON when --json is used.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
