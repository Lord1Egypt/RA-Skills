## Description:

Find evidence-backed xStocks in Mermail's published catalog and prepare one user-authorized USDC-to-xStock swap on Solana through PayBox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Mermail users can discover xStocks with catalog evidence or select an exact product for a one-time USDC purchase. A purchase requires the user's specified amount and PayBox review and signing; recommendations alone do not initiate a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recommendation could be mistaken for investment advice or purchase authorization.

Mitigation: Show catalog-backed evidence and keep discovery read-only until the user selects an exact product and USDC amount.

Risk: An incorrect amount, wallet, quote, or signing approval could cause financial loss.

Mitigation: Check the product, amount, wallet, quote, fees, and signing prompts before approving a transaction.

Risk: Retrying a pending or uncertain swap could create a duplicate transaction.

Mitigation: Reconcile the original provider request rather than submitting another swap.

## Reference(s):

- [Mermail skills documentation](https://docs.mermail.app/ai/skills)
- [Mermail xStocks catalog](https://xstock.mermail.app)
- [ClawHub skill listing](https://clawhub.ai/mermail/skills/mermail-xstocks-desk)
- [Tool map](artifact/references/tools.md)
- [Workflows](artifact/references/workflows.md)
- [Security boundaries](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with product evidence links and transaction status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to five catalog recommendations; purchase requests use PayBox review and signing.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
