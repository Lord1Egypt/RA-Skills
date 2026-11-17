## Description:

Splits a PDF into body-text Markdown plus an on-disk figure library and manifest so an agent can analyze the text first and inspect individual figures only when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjhveteran199-bit](https://clawhub.ai/user/xjhveteran199-bit)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and document-analysis agents use this skill to convert PDFs, especially scientific papers, into Markdown while extracting figures into indexed image files for selective follow-up inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents and extracted figures may include confidential information that remains in local output files.

Mitigation: Use the skill only when local extracted text and images are acceptable to retain, choose the output directory deliberately, and clean up generated files when needed.

Risk: Installing dependencies into system Python can affect the host environment.

Mitigation: Install markitdown and PyMuPDF in a dedicated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjhveteran199-bit/skills/pdf-extract-md-figs)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown and concise text guidance with shell commands; generated files include a Markdown body file, PNG figure files, and MANIFEST.txt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures are saved locally and are intended to be opened only on explicit request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
