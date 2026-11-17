## Description:

AI-powered HR Operating System for Southeast Asia with payroll, PH/SG/LK compliance, specialized HR agents, attendance, leave, overtime, expense workflows, and organization intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonypk](https://clawhub.ai/user/tonypk)

### License/Terms of Use:

MIT-0

## Use Case:

HR operators, managers, and employees use this skill to answer HR questions, calculate payroll and statutory contributions, generate HR documents, manage local team records, and connect to HalaOS for live employee, payroll, attendance, compliance, and analytics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access or modify sensitive employee, payroll, attendance, and compliance data.

Mitigation: Install only after review in real HR environments, use authorized HalaOS accounts, and scope API keys to the least privilege required.

Risk: Payroll, approval, attendance, or compliance-form actions may affect employees or official filings.

Mitigation: Require explicit human confirmation before executing payroll, approval, attendance, or compliance-form actions.

Risk: Native-mode local storage and user-provided HR data may include personal or payroll information.

Mitigation: Do not enter real employee or payroll data unless the selected storage location and privacy controls are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonypk/skills/halaos-hr)
- [HalaOS website](https://halaos.com)
- [Artifact GitHub link](https://github.com/tonypk/aigonhr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, structured summaries, inline commands, JSON examples, and HR document drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use HALAOS_API_KEY and local configuration for cloud-backed HR workflows; native mode can produce local calculations and documents without registration.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
