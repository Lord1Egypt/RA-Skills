## Description:

AI发票报销助手可从发票图片或描述中提取关键信息，分类费用，检查重复报销，并生成HTML报销报告、报销单和CSV导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance operators, and agent users use this skill to record invoices, organize reimbursement data, detect duplicate invoice numbers, and prepare reimbursement reports from locally stored records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoice and reimbursement records in local SQLite, CSV, and HTML outputs.

Mitigation: Use it only with invoice data suitable for local storage, restrict workspace access, and remove generated databases or exports when they are no longer needed.

Risk: Generated HTML reports and CSV exports can reflect invoice fields from user-provided inputs.

Mitigation: Do not open generated reports or CSV files from untrusted invoice data; escape report and CSV output before use in sensitive reimbursement workflows.

Risk: Delete and force-add operations can remove or overwrite invoice records.

Mitigation: Back up the local invoice database and add confirmation or recovery controls before using destructive commands on important records.

Risk: The artifact declares web tools and the generated report loads Chart.js from a CDN.

Mitigation: Review whether web permissions are needed, disclose the CDN dependency to users, or vendor a pinned local charting asset for restricted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/invoice-reimbursement)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command output, CSV exports, local SQLite files, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python; uses local SQLite storage and may generate local HTML and CSV files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
