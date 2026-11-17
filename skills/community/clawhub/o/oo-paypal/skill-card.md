## Description:

Operate PayPal through your OOMOL-connected account to read and manage orders, payments, balances, refunds, transactions, and shipment tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and PayPal account users use this skill to retrieve account, order, payment, refund, transaction, and shipment information, and to create or change PayPal records after reviewing the action and confirming its effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can install and refresh skills across other agents, creating a lasting side effect that the PayPal skill does not explain.

Mitigation: Review and approve the CLI's broader skill-management behavior before installation; configure OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill synchronization.

Risk: The installer, installed CLI binary, and hosted connector were not audited, and financial actions can change or remove PayPal records.

Mitigation: Review the installer separately, inspect the live action schema, and confirm the exact payload and effect before any write or destructive action.

## Reference(s):

- [PayPal API documentation: Orders v2](https://developer.paypal.com/docs/api/orders/v2/)
- [PayPal](https://www.paypal.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API responses, JSON, Guidance]

**Output Format:** [JSON PayPal action results and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read actions and state-changing actions; review the exact effect and confirm before writes or destructive changes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
