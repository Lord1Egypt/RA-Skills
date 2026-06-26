## Description: <br>
Reconciles Indian GST invoice CSVs with UPI transaction CSVs and produces matched, unmatched, and summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabh7464-hue](https://clawhub.ai/user/rishabh7464-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and accounting users in India use this skill to compare GST invoice exports against UPI collection statements, identify missing payments, and prepare month-end reconciliation outputs. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: GST and UPI exports can contain sensitive tax, payment, and customer information. <br>
Mitigation: Run the reconciliation locally on trusted CSVs and write reports to a private folder rather than a shared or synced location unless that is appropriate. <br>
Risk: Accounting or audit decisions may be wrong if source CSVs are incomplete, malformed, or mapped to unexpected columns. <br>
Mitigation: Review the generated unmatched reports and summary metrics against the source exports before relying on them for accounting or audit decisions. <br>


## Reference(s): <br>
- [CSV Schemas](references/csv-schemas.md) <br>
- [ClawHub release page](https://clawhub.ai/rishabh7464-hue/gst-upi-reconciliation-copilot-india) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated CSV and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-provided CSVs and writes reconciled, GST-unmatched, UPI-unmatched, and summary report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
