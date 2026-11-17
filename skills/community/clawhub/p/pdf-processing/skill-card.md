## Description:

Extracts text and tables from PDFs, fills PDF forms, and merges PDF documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainshow](https://clawhub.ai/user/rainshow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to extract PDF content, fill PDF forms, or merge PDF documents as part of document-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can affect the user's Python environment.

Mitigation: Install pdfplumber and pypdf in a virtual environment and avoid running pip as an administrator.

Risk: Form filling and document merging can modify or create user documents.

Mitigation: Confirm the target files and keep backups before using the skill for PDF modification or merge operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify or create PDF files when filling forms or merging documents.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
