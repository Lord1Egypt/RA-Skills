## Description:

Ofd Reader extracts text from OFD (Open Fixed-layout Document) files and converts document content to Markdown with basic paragraph, heading, and table structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanjian1972](https://clawhub.ai/user/zhanjian1972)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract text from OFD documents or convert OFD content to Markdown for review, indexing, and downstream editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional dependency installer invokes pip to install an external package.

Mitigation: Run the installer only when the optional dependency is needed and review the package source and environment policy first.

Risk: Processing untrusted OFD files may expose the agent environment to malformed ZIP or XML inputs.

Mitigation: Prefer trusted documents and process unknown files in a constrained workspace.

Risk: Supplying an output path can overwrite or create local files.

Mitigation: Choose deliberate output paths and review existing files before writing converted text or Markdown.

Risk: OFD layout, complex tables, and heuristic heading detection may not convert perfectly.

Mitigation: Review generated text or Markdown before using it as an authoritative representation of the source document.

## Reference(s):

- [OFD Format Reference](references/ofd-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown, with optional file output paths and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The conversion may write extracted text or Markdown to a caller-specified local output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
