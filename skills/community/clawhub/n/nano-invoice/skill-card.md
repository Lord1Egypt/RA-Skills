## Description:

Creates distinct exact-amount Nano (XNO) invoices, checks payments against the public ledger, and produces re-checkable receipts without holding keys or sending funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhyabi2](https://clawhub.ai/user/dhyabi2)

### License/Terms of Use:

MIT

## Use Case:

Merchants and their agents use this skill to associate Nano payments with individual orders, check settlement, and share verifiable receipts or refund guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wrong-amount payment can permanently close an invoice as underpaid or overpaid rather than leaving it open.

Mitigation: Confirm the exact settled amount before fulfilling an order; handle mismatches manually with a refund or a new invoice.

## Reference(s):

- [Nano Invoice on ClawHub](https://clawhub.ai/dhyabi2/skills/nano-invoice)
- [Default Nano RPC endpoint](https://rpc.nano.to)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invoice details, payment checks, verifiable receipts, and refund instructions; no funds are sent.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
