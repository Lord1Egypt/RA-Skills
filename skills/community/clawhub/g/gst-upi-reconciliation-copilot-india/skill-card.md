## Description:

Reconcile Indian GST invoice data with UPI transaction statements and produce audit-ready matched and unmatched reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabh7464-hue](https://clawhub.ai/user/rishabh7464-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, accountants, and finance operations teams use this skill to reconcile Indian GST invoice CSVs against UPI collection statements, generate matched and unmatched reports, and identify follow-up actions for month-end books or audit review.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Generated reports may contain sensitive financial records.

Mitigation: Use trusted GST and UPI exports only, write outputs to a private dedicated folder, and limit report sharing.

Risk: CSV report safety issues may affect spreadsheet review.

Mitigation: Sanitize CSV outputs for spreadsheet formulas before opening or sharing them.

Risk: Reconciliation integrity may be affected by missing statuses or duplicate or blank invoice numbers.

Mitigation: Validate missing statuses plus duplicate or blank invoice numbers before using reports for books, collections, or audit decisions.

## Reference(s):

- [CSV Schemas](references/csv-schemas.md)
- [ClawHub Skill Page](https://clawhub.ai/rishabh7464-hue/skills/gst-upi-reconciliation-copilot-india)
- [Publisher Profile](https://clawhub.ai/user/rishabh7464-hue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, CSV report files, and JSON summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates reconciled CSV rows, GST-unmatched CSV rows, UPI-unmatched CSV rows, a summary JSON report, and human-facing next actions for unmatched records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
