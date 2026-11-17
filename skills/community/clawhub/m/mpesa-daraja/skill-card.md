## Description:

Advisory reference for Safaricom M-Pesa Daraja integration planning, reviews, sandbox testing, callbacks, reconciliation, and production-readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevilpaulo](https://clawhub.ai/user/nevilpaulo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, review, test, and prepare Safaricom M-Pesa Daraja payment integrations. It focuses on sandbox-first workflows, callback handling, reconciliation, and production-readiness guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-integration guidance could be applied to live payment, payout, reversal, or customer-facing flows without sufficient approval.

Mitigation: Require explicit approval before any live Daraja request and default to sandbox endpoints and placeholder configuration.

Risk: Real Daraja credentials, phone numbers, transaction IDs, receipt numbers, or callback payloads could leak through generated examples, logs, or committed files.

Mitigation: Keep sensitive values in protected deployment settings, use placeholders in examples, and mask payment and personal data in logs.

Risk: Callback retries or duplicate Daraja events could double-credit or incorrectly transition payment state.

Mitigation: Persist callbacks durably, deduplicate by Daraja request and transaction identifiers, and couple fulfillment to confirmed idempotent state transitions.

Risk: Endpoint names, versions, fields, or sandbox behavior may drift from the bundled reference snapshot.

Mitigation: Verify current Safaricom Daraja documentation before production work or skill updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nevilpaulo/skills/mpesa-daraja)
- [Daraja Endpoint Reference](references/api-endpoints.md)
- [M-Pesa Daraja Examples](references/examples.md)
- [STK Push / Lipa na M-Pesa Online](references/stk-push.md)
- [Production Readiness](references/production-readiness.md)
- [M-Pesa Daraja Test Cases](references/test-cases.md)
- [Skill Maintenance](references/maintenance.md)
- [Safaricom Daraja Developer Portal](https://developer.safaricom.co.ke/)
- [Safaricom Developer API Catalogue](https://developer.safaricom.co.ke/api/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; live payment, payout, reversal, or customer-facing requests require explicit approval.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
