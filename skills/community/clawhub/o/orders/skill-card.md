## Description:

Track orders locally. Use when creating orders, checking status, updating quantities, canceling, or generating sales reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operational users can use this skill to create, list, update, cancel, and report on local order records from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order, customer, pricing, notes, and cancellation data are stored locally in ~/.orders/orders.json.

Mitigation: Use the skill only on trusted accounts, keep home directory and orders file permissions restrictive, and avoid storing sensitive data unnecessarily.

Risk: CSV exports may be opened in spreadsheet software when order fields contain untrusted text.

Mitigation: Review and sanitize user-provided fields before opening CSV exports in spreadsheet tools.

## Reference(s):

- [ClawHub Orders skill page](https://clawhub.ai/xueyetianya/skills/orders)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, json, csv, shell commands]

**Output Format:** [Plain text, JSON, or CSV printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores order data locally in ~/.orders/orders.json.]

## Skill Version(s):

3.4.1 (source: server release metadata; artifact frontmatter reports 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
