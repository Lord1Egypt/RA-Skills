## Description:

lawclaw helps attorneys, paralegals, and legal operations teams analyze local legal documents by extracting PDF text, finding clauses, comparing redlines, checking citations, and searching discovery sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagadeeshmurali-coder](https://clawhub.ai/user/jagadeeshmurali-coder)

### License/Terms of Use:


## Use Case:

External legal professionals use this skill for contract review, litigation support, due diligence, e-discovery, privilege log support, transcript analysis, and brief citation checks on local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document-processing commands can read, search, create, or rename legal case files.

Mitigation: Review commands before execution, especially recursive searches, output generation, and batch renames; keep backups or audit trails for case files.

Risk: Extracted PDF or OCR text can be inaccurate and may affect legal analysis or filings.

Mitigation: Verify extracted text, OCR output, and citations against authoritative source documents before relying on them.

Risk: Legal documents may contain privileged, confidential, or personally identifiable information.

Mitigation: Run workflows locally, maintain privilege logs where appropriate, redact sensitive data before production, and do not transmit client data to external services without written consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jagadeeshmurali-coder/skills/lawclaw)
- [Declared homepage](https://github.com/legal-tools/lawclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local legal-document processing workflows and may include command examples that read, search, convert, compare, create, or rename local files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
