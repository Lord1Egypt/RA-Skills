## Description:

Convert PDF to Markdown using local processing. No external API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert local PDF documents into clean Markdown without external API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party Python package pdfplumber, and the release evidence notes that the dependency is unpinned.

Mitigation: Install in a least-privileged environment and review or pin the pdfplumber version before using the skill with sensitive PDFs.

Risk: The skill reads local PDFs and can write Markdown output files.

Mitigation: Grant access only to the intended input PDF and output location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifei68801/skills/pdf2md-clean)
- [Publisher profile](https://clawhub.ai/user/lifei68801)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown text or a Markdown file generated from a local PDF]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local file read access to the input PDF and optional file write access for the Markdown output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
