## Description:

Reads text-extractable PDF files and produces a structured summary with document basics, core sections, key data, conclusions, and suggested actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read uploaded PDF documents and generate concise, structured summaries for review. It is most suitable for Chinese or English text-based PDFs where local text extraction is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a publishing script with a hard-coded ClawHub token and broad upload behavior.

Mitigation: Review or remove upload.sh before installation, rotate the exposed token, and confirm the package contents are limited to intended skill files.

Risk: The tool processes local PDFs through a PyMuPDF subprocess.

Mitigation: Use it only with PDFs the operator is comfortable processing locally, and keep the runtime dependency and file access scope reviewed.

Risk: Summaries may be biased toward Chinese resume-style sections and may miss structure in unrelated document types.

Mitigation: Review generated summaries against the source PDF before using them for decisions or downstream reporting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/banalit/skills/luke-pdf-read-summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summary with document metadata, section bullets, key data, conclusions, and suggested actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is generated from locally extracted PDF text and may reflect Chinese resume-style extraction heuristics.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
