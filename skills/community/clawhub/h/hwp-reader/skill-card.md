## Description:

Extracts and analyzes text, tables, images, and metadata from Korean HWP and HWPX documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read and analyze Korean Hangul Word Processor files, including government forms, templates, and document revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency behavior or version drift in pyhwp can affect legacy HWP extraction.

Mitigation: Use a virtual environment and pin or review pyhwp before installing it.

Risk: Very large or untrusted HWPX files can consume excessive memory, CPU, or output budget during ZIP and XML parsing.

Mitigation: Run extraction with memory, CPU, and output limits before using the resulting text in downstream workflows.

Risk: Text-mode extraction can omit or simplify document structure, formatting, encrypted content, and some table details.

Mitigation: Treat extracted text as a working representation and manually review source documents when formatting, tables, or protected sections matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/hwp-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with extracted document text, analysis, and inline Python or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact author line)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
