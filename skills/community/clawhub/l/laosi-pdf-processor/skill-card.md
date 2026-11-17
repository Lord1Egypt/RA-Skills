## Description:

Processes PDFs for text extraction, table recognition, document merging, page splitting, metadata reading, and password-protected files using a Python implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users can use this skill to extract text and metadata from PDFs, split or merge documents, and manage batch PDF processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processed PDFs may leave snippets or metadata in a persistent job log.

Mitigation: Avoid sensitive PDFs unless the job log is removed, disabled, or access-controlled.

Risk: Large or complex PDFs can consume excessive resources during parsing.

Mitigation: Use bounded file-size and page-count limits before processing files.

Risk: PDF parsing dependencies can introduce supply-chain or parser risk.

Mitigation: Install dependencies in an isolated environment with pinned versions and review the code before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-pdf-processor)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-like operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PDF output files and a local PDF job log when the generated implementation is used.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
