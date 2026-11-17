## Description:

Safely operate the nova CLI wallet for authentication, balance checks, sending funds, withdrawals, and key management across mainnet and testnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthluvr](https://clawhub.ai/user/synthluvr)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate the nova wallet CLI for balance checks, authentication, stablecoin transfers, claim links, withdrawals, and key management while applying confirmations, structured-output parsing, and secret-handling safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party wallet CLI that can move funds and handle wallet secrets.

Mitigation: Review the nova CLI package and publisher trust before installing; prefer a pinned, reviewed version and avoid global installation where possible.

Risk: Send and withdrawal commands can submit real financial transactions and may be non-idempotent.

Mitigation: Use dry runs first, confirm amount, destination, blockchain, and network with the user, and never retry financial commands blindly.

Risk: Private keys, seed phrases, and claim URLs expose wallet access or funds if logged or shared.

Mitigation: Do not store, log, or paste secrets into shared or persistent contexts; warn before export operations and treat claim URLs as credentials.

Risk: The selected network persists across sessions and mainnet/testnet confusion can affect real funds.

Mitigation: Check `nova config get network` before any financial action and require explicit confirmation of the intended network.

## Reference(s):

- [nova CLI reference](references/REFERENCE.md)
- [Nova project homepage](https://github.com/MynthAI/nova)
- [Nova npm package](https://www.npmjs.com/package/@mynthai/nova)
- [ClawHub Nova skill page](https://clawhub.ai/synthluvr/skills/nova)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON/TOON parsing expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 24+ and internet access; emphasizes dry runs, explicit confirmations, exit-code checks, and secret handling.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
