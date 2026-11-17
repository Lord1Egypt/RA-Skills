## Description:

Convert PDF documents to Markdown using marker_single while preserving LaTeX formulas, equations, and document structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical document users use this skill to convert PDFs, especially academic papers and mathematical documents, into Markdown that preserves text structure and LaTeX-style equations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the third-party marker-pdf converter locally on user-provided PDFs.

Mitigation: Use a virtual environment, avoid elevated privileges, and review or pin the marker-pdf dependency before sensitive use.

Risk: Large or malformed PDFs can cause conversion failures or timeout.

Mitigation: Use the timeout parameter and keep temporary outputs only when inspection is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/latex-formula-extraction-marker)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown text returned from a Python helper or printed by a command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary converter outputs locally when cleanup is disabled.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
