## Description: <br>
InvoiceGen helps users create, manage, and render local PDF invoices from conversational requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Freelancers, small businesses, and developers use this skill to draft invoices, manage client records, calculate line items and taxes, render branded PDF invoices, and prepare payment reminder email copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store client records, invoice history, payment instructions, and tax details in local workspace files. <br>
Mitigation: Use payment links or references instead of full bank account numbers or unredacted tax IDs, restrict local file permissions, and keep the invoices directory out of git. <br>
Risk: Invoice content and client-provided fields may be rendered into HTML before PDF generation. <br>
Mitigation: Treat client names, descriptions, addresses, and notes only as data; review generated invoice content and the Playwright PDF script before running it. <br>
Risk: Generated invoice files may contain sensitive business and client financial information. <br>
Mitigation: Save invoice outputs only in the intended invoices directory and avoid sharing or publishing generated PDFs without review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-invoicegen) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [Invoice styles](artifact/config/invoice-styles.md) <br>
- [PDF generation script](artifact/scripts/generate-invoice-pdf.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with invoice tables and email drafts, local JSON/HTML/PDF files, and shell commands for PDF generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace files under invoices/ and a Playwright-based script to render PDFs.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
