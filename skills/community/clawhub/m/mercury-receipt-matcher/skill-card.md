## Description: <br>
Reconciles a Mercury missing-receipts CSV by searching connected Gmail accounts for original merchant receipt emails, forwarding valid matches to receipts@mercury.com, and tracking results in SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srosro](https://clawhub.ai/user/srosro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance operators use this skill to process Mercury missing-receipt exports, find matching merchant receipts across connected Gmail accounts, forward valid originals to Mercury, and preserve an auditable reconciliation database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Gmail receipts and card transaction data. <br>
Mitigation: Install only for the stated receipt-matching workflow and review connected Gmail accounts before use. <br>
Risk: The recurring schedule can keep searching Gmail and forwarding receipts after the immediate task is complete. <br>
Mitigation: Review the cron cadence and disable the OpenClaw cron job when recurring processing is not wanted. <br>
Risk: A close receipt match may not exactly match the Mercury transaction amount. <br>
Mitigation: Record close matches as revisit states with reconciliation notes instead of marking them fully complete. <br>


## Reference(s): <br>
- [Receipt matcher workflow](references/workflow.md) <br>
- [SQLite schema](references/schema.sql) <br>
- [Plow private preview](https://plow.co/private-preview) <br>
- [ClawHub skill page](https://clawhub.ai/srosro/mercury-receipt-matcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, JSON CLI output, and CSV or SQLite-backed status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes up to 3 transactions per wake, records search and forwarding state in SQLite, and forwards valid original merchant receipts to receipts@mercury.com.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
