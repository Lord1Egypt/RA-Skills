## Description:

Parse and extract content from .docx, .pdf, and .txt documents, including plain text and tables for document analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjk39966-glitch](https://clawhub.ai/user/mjk39966-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to parse uploaded Word, PDF, and text documents before summarizing, answering questions, extracting tables, or searching document content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsing confidential or regulated documents may expose sensitive content to the local runtime or downstream agent responses.

Mitigation: Use only in a trusted local environment, prefer a virtual environment, and avoid confidential or regulated documents unless the runtime and handling process are approved.

Risk: The OpenClaw entry file is less capable than the documented parse_document.py script, which may cause inconsistent behavior depending on the entry point used.

Mitigation: Use scripts/parse_document.py for the documented JSON and text parsing workflow, and verify extracted output before relying on answers.

Risk: Scanned PDFs, image-only documents, and complex layouts may produce incomplete or missing extraction results.

Mitigation: Confirm PDFs contain selectable text and review extracted text and tables before analysis.

## Reference(s):

- [Document Parser Usage Examples](artifact/references/usage_examples.md)
- [ClawHub skill page](https://clawhub.ai/mjk39966-glitch/skills/mjk39966-document-parser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or plain-text parser output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extracted document text, tables, and metadata; output quality depends on document format and parser support.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
