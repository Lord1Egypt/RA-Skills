## Description:

Professional invoice generation for freelancers and small businesses, with local client records, payment tracking, recurring templates, and revenue reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Freelancers, consultants, indie creators, and small businesses use this skill to generate and track local invoices, manage client records, apply taxes and discounts, create recurring invoices, and run basic revenue or overdue-payment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML invoices can include unescaped active browser content when populated with untrusted client data.

Mitigation: Review before using with untrusted client data and treat generated HTML invoices as active browser content until escaping is fixed.

Risk: Custom invoice numbers can write files outside the intended output folder.

Mitigation: Do not accept custom invoice numbers from untrusted sources; keep invoice generation in an isolated working directory.

Risk: The local data directory stores business ledger data and can be exposed if shared through cloud sync, SSH, or a server without separate controls.

Mitigation: Keep the data directory private, add access controls before any remote exposure, and maintain independent backups.

Risk: Tests and command examples create local data and output files.

Mitigation: Run tests only in an isolated folder.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/invoice-forge)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)
- [License](artifact/LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated invoice files can be HTML, Markdown, or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local JSONL client and invoice records; generated invoice files are saved under the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
