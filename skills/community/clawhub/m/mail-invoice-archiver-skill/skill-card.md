## Description: <br>
Reads supported mailbox providers such as 126, 163, and Gmail, identifies invoice attachments or invoice download links, archives invoices by month, deduplicates by invoice number and amount, and prepares monthly reports plus delivery bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents that manage invoice workflows use this skill to sync supported mailboxes, identify invoice attachments or links, deduplicate invoices, archive them by month, and prepare monthly reports and delivery bundles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and local invoice archives. <br>
Mitigation: Use system credential storage or environment variables when possible, avoid plaintext config secrets, and keep real Feishu credentials outside the published skill directory. <br>
Risk: The skill may automatically follow invoice download links from email. <br>
Mitigation: Configure a narrow trusted domain list, or use no-follow-links or a sandboxed environment when processing untrusted mail. <br>
Risk: Invoice extraction, attachment conversion, and deduplication can misclassify files or surface conflicts. <br>
Mitigation: Review monthly report totals, high-value invoices, duplicate groups, conflicts, and failures before relying on the archive. <br>


## Reference(s): <br>
- [Compatibility Notes](references/compatibility-notes.md) <br>
- [Mail Invoice Archiver on ClawHub](https://clawhub.ai/amortalsodyssey/mail-invoice-archiver-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local invoice archives, monthly reports, duplicate and conflict summaries, and delivery bundle paths through CLI-backed workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
