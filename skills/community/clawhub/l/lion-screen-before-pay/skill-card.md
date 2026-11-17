## Description:

Screens x402 payTo wallets with LION before USDC payment and rechecks repeat counterparties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8dp6brm9hp-svg](https://clawhub.ai/user/8dp6brm9hp-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents screening a counterparty wallet before an x402 payment use the LION verdict to decide whether to proceed, and recheck repeat counterparties before paying again.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening shares the payTo wallet or related domain with LION and incurs paid checks.

Mitigation: Use only when comfortable sharing counterparty details and paying the disclosed $0.001 initial and $0.01 repeat check fees.

Risk: Optional unpinned npm/npx helpers run in a sensitive payment workflow.

Mitigation: Pin package versions and review the helper before use.

## Reference(s):

- [LION receipt verification key](https://lionx402.com/.well-known/lion-compliance-key.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes paid initial and repeat checks and retention of signed receipts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
