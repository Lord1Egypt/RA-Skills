## Description:

A payment skill powered by the mypay-bot CLI for payment, purchase, checkout, transfer, wallet, and transaction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhc1111](https://clawhub.ai/user/xhc1111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare and execute mypay-bot payment workflows, including intent capture, wallet checks, and payment submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit payments without a final transaction-specific confirmation.

Mitigation: Require a clear final confirmation of the exact transaction details before any submit-payment command is run.

Risk: Payment links or tokenized URLs may expose sensitive payment material when copied in full.

Mitigation: Avoid sharing full payment URLs or tokenized links unless the recipient is trusted and disclosure is necessary.

Risk: The workflow depends on mypay-bot and wallet-signing credentials.

Mitigation: Use this skill only when the mypay-bot CLI is trusted and credentials are stored and scoped appropriately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhc1111/skills/my-pay)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, node, npm, the mypay-bot CLI, MYPAY_API_KEY, and MYPAY_WALLET_SECRET; payment links and command output may include sensitive tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
