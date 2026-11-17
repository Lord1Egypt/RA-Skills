## Description:

Invoice Agent helps freelancers, agencies, and small businesses create, track, export, and summarize local invoices, including multi-currency tax calculations, HTML invoice generation, overdue tracking, and payment reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atum246](https://clawhub.ai/user/atum246)

### License/Terms of Use:

Proprietary

## Use Case:

External users such as freelancers, agencies, and small businesses use this skill to manage local client billing workflows: create invoices, update payment status, export invoice JSON, generate HTML invoices, produce reminders, and review financial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive billing and client data locally under ~/.invoice-agent.

Mitigation: Use it only on trusted machines and manage local file permissions, backups, and retention for billing data.

Risk: Generated HTML invoices may include unescaped user-controlled invoice fields.

Mitigation: Use trusted invoice data, review generated HTML before sharing it, and escape fields before rendering imported or untrusted invoice content.

Risk: Payment reminder text includes escalation language that may not fit every business or legal context.

Mitigation: Review and edit reminder text before sending it to clients.

Risk: The delete --force workflow can permanently remove non-draft invoice records.

Mitigation: Back up local invoice data before force deletion and use the option only when permanent removal is intended.

## Reference(s):

- [Invoice Agent Reference Guide](references/guide.md)
- [Invoice HTML Template](assets/invoice-template.html)
- [ClawHub Skill Page](https://clawhub.ai/atum246/skills/invoice-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI scripts produce JSON records, reminder text, and HTML invoice files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores invoice and billing data locally under ~/.invoice-agent.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact skill-meta.yaml reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
