## Description:

Extract structured data from academic papers in PDF, DOCX, or TXT format into XLSX or CSV literature review tables with fidelity checks, batch support, and multi-domain handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2025biophilia-coder](https://clawhub.ai/user/2025biophilia-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to extract paper metadata, methods, findings, confidence scores, and source notes into structured literature review tables. It supports single-paper and batch workflows for English and Chinese papers across psychology, cognitive neuroscience, computer science, and brain science.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet cells may contain untrusted values from papers and are written without formula neutralization.

Mitigation: Review or neutralize generated spreadsheet values before opening outputs in spreadsheet software, especially when processing untrusted papers.

Risk: Batch logs may retain excerpts or metadata from processed papers.

Mitigation: Avoid confidential papers unless logging is reduced and output directories are protected according to the data sensitivity.

Risk: Low-confidence or ambiguous extractions may be incomplete or misleading.

Mitigation: Review confidence scores, source notes, and the quality checklist before relying on populated review tables.

## Reference(s):

- [Extraction Patterns for Paper-to-Table](references/extraction-patterns.md)
- [Quality Checklist for Paper-to-Table](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with bash commands, structured JSON extraction records, and XLSX or CSV table outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch runs can generate processing reports and logs; extracted fields include confidence and source notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
