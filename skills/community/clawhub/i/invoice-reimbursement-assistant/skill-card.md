## Description:

Collects invoice attachments from email, verifies invoices, categorizes expenses, validates invoice headers, and generates reimbursement spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningmengyun12366](https://clawhub.ai/user/ningmengyun12366)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and finance teams use this skill to collect invoice attachments from mailbox accounts, run invoice verification, classify expenses, validate company invoice headers, and produce reimbursement spreadsheets and archived invoice files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide mailbox access credentials and an invoice verification API key.

Mitigation: Use the skill only when the publisher is trusted, avoid sharing secrets in logs or persistent files, and prefer platform-managed secret storage or OAuth where available.

Risk: The installation flow downloads and runs remote native binaries that are not hash-pinned or independently signed in the artifact evidence.

Mitigation: Verify downloaded executables through an independent trusted channel before execution and restrict downloads to the single platform binary required for the current OS and CPU.

Risk: The skill includes broad installation and update authority over its installed skill directory.

Mitigation: Require explicit user confirmation before modifying installed skill files, keep backups during updates, and review the installed files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningmengyun12366/skills/invoice-reimbursement-assistant)
- [Publisher profile](https://clawhub.ai/user/ningmengyun12366)
- [Installation and update documentation](https://download.ningmengyun.com/Skills/invoice-reimbursement-assistant/invoice-reimbursement-assistant-install.md)
- [NMY AI Tax Open Platform](https://www.nmy.cn)
- [Invoice verification API endpoint](https://openapi.nmy.cn/api/v1/skill/national-invoice-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, JSON command output expectations, generated keywords JSON, reimbursement XLSX spreadsheets, and archived invoice files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects runtime mailbox credentials and an invoice verification API key, and its command stdout is expected to be parseable JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog; artifact frontmatter and install documentation state 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
