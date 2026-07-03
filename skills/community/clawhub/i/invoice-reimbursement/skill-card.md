## Description: <br>
发票报销助手 helps agents record invoice details, classify expenses, detect duplicate invoices, and generate reimbursement reports from local invoice data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance staff, and developers can use this skill to organize invoice reimbursement workflows, including invoice entry, duplicate checks, category summaries, CSV export, and HTML reimbursement reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local invoice records can be permanently changed or deleted by delete and force-add commands. <br>
Mitigation: Back up the local SQLite database before bulk edits, review invoice IDs before deletion, and avoid force operations unless duplicate replacement is intended. <br>
Risk: Generated HTML reports can contain sensitive invoice data and load a charting script from a CDN. <br>
Mitigation: Open reports only in trusted environments and replace the CDN dependency with a local bundled chart library before using reports with sensitive reimbursement data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/invoice-reimbursement) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands, generated HTML reports, CSV exports, and local SQLite records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite storage for invoice records; generated HTML reports may load Chart.js from jsDelivr unless the dependency is replaced locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
