## Description:

Mercury bank API for Digital 4 Jesus LLC account balances, transactions, invoices, customers, recipients, organization details, and money movement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godsboy](https://clawhub.ai/user/godsboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with authorization for the relevant Mercury account use this skill to inspect banking data and manage accounts receivable workflows such as invoices and customers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read banking data and modify accounts receivable or payment records.

Mitigation: Install only for authorized Mercury accounts, use a least-privileged token, keep the secrets file private, and require explicit confirmation before every write action.

Risk: Invoice creation contains an argument-injection flaw according to the authoritative security scan summary.

Mitigation: Fix the invoice argument handling before use with untrusted input, and review generated invoice values before executing create or update commands.

Risk: The Mercury API token may be exposed through process arguments or local secret handling.

Mitigation: Avoid passing tokens on command lines, restrict permissions on ~/.secrets/mercury.env, and rotate credentials if exposure is suspected.

## Reference(s):

- [Mercury API Reference](references/api.md)
- [Mercury API Base URL](https://api.mercury.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/godsboy/skills/mercury-bank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON examples, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Mercury API helper commands that return formatted JSON or account summaries when credentials are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
