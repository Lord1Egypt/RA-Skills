## Description:

Parses local PDF files into structured Markdown and JSON using opendataloader-pdf for deterministic, local document content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trshdesigns](https://clawhub.ai/user/trshdesigns)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert local PDFs into Markdown and JSON files for document ingestion and RAG workflows. It is intended for deterministic local parsing of PDFs that the user chooses to process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party Python package.

Mitigation: Install opendataloader-pdf only from a trusted Python package source, preferably in an isolated environment with a pinned dependency version.

Risk: The script accepts user-provided input and output paths, and the output directory is not independently constrained by the wrapper.

Mitigation: Run the skill only on PDFs you intend to parse and choose an output directory inside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trshdesigns/skills/pdf-parser-agent)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON files with terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local output files under the selected output directory; the default output directory is output/parsed_pdf.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
