## Description:

Convert PDF files to Markdown with table recognition. Use when extracting text, converting tables, summarizing documents, fixing formatting issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to extract text from PDF files, convert PDFs or copied PDF text into Markdown, identify headings, convert table-like regions, inspect PDF metadata, and export local conversion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted filenames can be expanded into Python code during fallback PDF processing.

Mitigation: Review and fix the fallback path handling so file paths are passed into Python as data; avoid processing untrusted filenames until that is addressed.

Risk: Converted document content and command history are stored on the local machine.

Mitigation: Use an appropriate PDF_TO_MARKDOWN_DIR for sensitive work and review or clear generated outputs and history according to local data-handling requirements.

## Reference(s):

- [Markdown Syntax Reference](artifact/tips.md)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write converted output, export files, configuration, and command history to a local data directory.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
