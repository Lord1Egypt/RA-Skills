## Description:

Jubilee Skill helps agents manage treasury funds across Base, Solana, and Ethereum using Jubilee Protocol vault status, balance, deposit, withdrawal, yield donation, and reporting commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prayingperceptions](https://clawhub.ai/user/prayingperceptions)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to inspect vault status, manage balances, deposit or withdraw treasury assets, donate yield, and generate treasury health reports for AI agents using Jubilee Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill with a funded wallet can trigger irreversible treasury transfers if chain, token, amount, vault, recipient, or signer values are wrong.

Mitigation: Use a limited-balance operational wallet or managed signer and independently verify every chain, token, amount, vault, and recipient value before execution.

Risk: Private key handling is critical because the skill describes wallet-based treasury operations.

Mitigation: Keep wallet files and private keys out of source control and use managed signer controls where available.

Risk: Recurring donation automation can spend funds without timely human review.

Mitigation: Do not run scheduled donation automation unless spending limits, recipient allowlists, alerts, and manual approval controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prayingperceptions/skills/openclaw-skill-jubilee)
- [Jubilee Protocol documentation](https://docs.jubileeprotocol.xyz)
- [Jubilee Protocol GitHub](https://github.com/Jubilee-Protocol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide real-money wallet, vault, transfer, and recurring donation operations; review all values before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
