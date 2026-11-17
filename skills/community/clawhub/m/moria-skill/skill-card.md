## Description:

Moria Skill helps an OpenClaw agent manage Moria.fun wallet and token workflows, including token creation, minting, trading, refunds, fee claims, deposits, and balance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyeon9057](https://clawhub.ai/user/miyeon9057)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure a Moria.fun wallet and run token-management workflows such as creating tokens, buying and selling tokens, claiming fees, and checking balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign real Web3 transactions while handling wallet secrets.

Mitigation: Do not use a funded wallet until wallet signing, key storage, and transaction preview controls have been reviewed and hardened.

Risk: Wallet codes and provider credentials may be exposed through command arguments, local files, logs, or errors.

Mitigation: Rotate hard-coded provider credentials, protect wallet-code input, mask secrets in all outputs, and avoid echoing raw config or error payloads.

Risk: Asset-moving actions such as create, mint, buy, sell, refund, and claim can move funds or tokens without sufficient preview.

Mitigation: Require explicit transaction previews and user confirmation before each asset-moving command.

Risk: The artifact behavior can delete user-provided upload files after token creation.

Mitigation: Delete user-provided files only after clear user approval or after copying them to a safe temporary location.

## Reference(s):

- [Moria Skill security policy](references/security.md)
- [Moria.fun](https://moria.fun)
- [ClawHub skill page](https://clawhub.ai/miyeon9057/skills/moria-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and command output such as tables, public wallet addresses, URLs, and transaction signatures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on wallet configuration, network state, and user-provided token or image inputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; package.json reports 0.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
