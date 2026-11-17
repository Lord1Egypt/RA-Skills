## Description:

PDF万能大师 helps agents inspect, convert, OCR, edit, protect, compress, merge, split, redact, and summarize PDF documents using documented workflows and local Python utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ford828](https://clawhub.ai/user/ford828)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Employees, external users, and developers use this skill to turn PDF requests into guided document-processing workflows, including conversion, OCR, editing, batching, redaction, compression, review, and Feishu-oriented handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk redaction and protection workflows can give unsafe or misleading assurances about sensitive documents.

Mitigation: Review before installing for sensitive or regulated documents, use redaction only on copies, manually inspect scanned or image pages, and verify deletion certificates before sharing them.

Risk: Sensitive-document workflows may expose confidential content if routed to cloud processing or stored in unintended outputs.

Mitigation: Confirm where Feishu outputs, backups, logs, and certificates will be stored, keep sensitive processing local when required, and avoid persisting passwords or sensitive identifiers in logs.

Risk: PDF protection, signing, invoice validation, and contract review can be misunderstood as legal or authoritative guarantees.

Mitigation: Use strong owner passwords for protected PDFs, clearly label unavailable validation or signing services, and require human review for legal, financial, or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ford828/skills/pdf-master)
- [README](README.md)
- [Core capability procedures](references/capabilities-core.md)
- [Value capability procedures](references/capabilities-value.md)
- [Advanced capability procedures](references/capabilities-pro.md)
- [Command guide](references/command-guide.md)
- [Error handling and fallback strategy](references/error-handling.md)
- [Quality standards](references/quality-standards.md)
- [Security and compliance guardrails](references/security-compliance.md)
- [Technical specification](references/tech-spec.md)
- [OCR configuration guide](references/ocr-config.md)
- [Feishu setup guide](references/feishu-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file outputs, reports, command snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce processed PDFs, spreadsheets, OCR text, audit reports, deletion certificates, and handoff instructions depending on the requested workflow.]

## Skill Version(s):

2.1.0 (source: server release metadata, artifact metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
