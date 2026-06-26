## Description: <br>
Nex Einvoice helps agents create, manage, validate, and export Belgian e-invoices in Peppol BIS 3.0 UBL XML from Dutch or English natural-language or structured inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, small Belgian businesses, and their agents use this skill to draft invoices, manage customer and seller billing data, calculate Belgian VAT, track payment status, and export UBL XML for accounting workflows. <br>

### Deployment Geography for Use: <br>
Belgium <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive invoice, customer, seller, and payment data may be stored locally in plaintext. <br>
Mitigation: Install and run only in an environment where local plaintext business and payment data storage is acceptable; avoid entering unnecessary sensitive data. <br>
Risk: The release may overstate encryption, live VAT validation, PDF export, reminders, credit-note workflow, and compliance guarantees. <br>
Mitigation: Independently verify required invoicing, tax, and compliance outputs before relying on them for business records or regulatory filing. <br>
Risk: Agent actions can create invoices, save contacts, export XML, or change invoice status. <br>
Mitigation: Require explicit user confirmation before running commands that create, persist, export, or mutate invoice data. <br>


## Reference(s): <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-einvoice) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, XML, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the underlying CLI returns plain text, JSON, or UBL XML and can write XML export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local invoice, contact, seller, and payment data; commands may create or update records and write exports under the user's local data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
