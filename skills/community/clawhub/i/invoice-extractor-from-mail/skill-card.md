## Description:

Designed for AP finance teams in cross-border trade enterprises, this skill fetches invoice attachments from email or local files, extracts key invoice fields with ADP, and exports results to Excel or business systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeane-li](https://clawhub.ai/user/jeane-li)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

AP finance, audit, and finance IT teams use this skill to collect invoice attachments from mailboxes or local folders, extract structured invoice and receipt data, and prepare Excel exports or business-system payloads for reconciliation, settlement, audit, reimbursement, and ERP entry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or invoke external ADP CLI tooling before processing invoices.

Mitigation: Review or replace installer paths, pin dependency versions, and require explicit approval before dependency installation.

Risk: The workflow handles sensitive mailbox, invoice, cloud-storage, and ERP credentials.

Mitigation: Use a least-privilege mailbox or folder, narrow sender and date filters, and store credentials in an approved secret manager instead of plaintext configuration where possible.

Risk: Invoice files are transmitted to ADP for extraction.

Mitigation: Confirm ADP data-processing compliance before processing sensitive or regulated documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeane-li/skills/invoice-extractor-from-mail)
- [ADP Portal - Chinese Mainland](https://adp.laiye.com/?utm_source=clawhub)
- [ADP Portal - Outside Chinese Mainland](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [ADP Invoice/Receipt Field Schema Reference](refers/adp-invoice-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and structured output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces invoice extraction workflow guidance, field mapping instructions, Excel export conventions, API push guidance, and error-handling recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
