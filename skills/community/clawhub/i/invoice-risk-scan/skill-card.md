## Description:

Checks invoice tax-ID format, positive amount, and date format and year before reimbursement or booking, returning pass/fail results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Finance staff and developers use this skill to screen invoice fields before reimbursement or booking and route flagged entries for review. It is a preliminary check, not tax or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad tool access and inconsistent permission disclosures despite a local field-checking script.

Mitigation: Review tool access before installation; remove unused Write and WebFetch permissions or justify them, and align the documentation with actual behavior.

Risk: Simple field checks can miss invalid invoices, and the documented file input and configurable blocking are not implemented by the script.

Mitigation: Use supported command-line fields only, review flagged and passed invoices through normal finance controls, and explicitly handle failure exit codes in any workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/invoice-risk-scan)
- [LGD theory (background reference)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable check results or JSON with pass, checks, and problems]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes: 0 for pass, 1 for failed checks, 2 for invalid usage.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled documentation says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
