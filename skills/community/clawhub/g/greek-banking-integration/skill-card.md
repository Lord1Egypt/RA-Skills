## Description:

Parses bank statements from all major Greek banks (Alpha, NBG, Eurobank, Piraeus). File-based CSV/Excel import with transaction reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

External users, developers, and accounting teams use this skill to process exported Greek bank statement files, reconcile transactions, categorize VAT-related activity, and generate accounting-ready reports or exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial records such as bank statements, transaction histories, reconciliation data, and accounting exports.

Mitigation: Use it only in a controlled workspace and keep imported statements, processed data, and exports access-restricted.

Risk: Optional Xero integration can push accounting data to an external service when XERO_API_KEY is configured.

Mitigation: Avoid configuring XERO_API_KEY unless direct external submission is intended and approved.

Risk: Automatic updates, scheduled processing, or accounting-system write operations can affect financial records.

Mitigation: Require human review before auto-update, scheduled processing, or accounting-system write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/greek-banking-integration)
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated CSV, JSON, reconciliation reports, VAT analysis, and accounting-software export files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
