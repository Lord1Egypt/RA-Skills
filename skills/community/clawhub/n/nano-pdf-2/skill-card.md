## Description:

PDF精简工具 helps agents use the nano-pdf CLI to edit, convert, merge, compress, and extract content from PDF files with natural-language instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document operators, and knowledge workers use this skill to ask an agent to prepare or run nano-pdf CLI workflows for PDF editing, conversion, merging, compression, and extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file write authority while also describing broader workflow automation beyond PDF CLI usage.

Mitigation: Grant permissions narrowly, constrain the agent to specific nano-pdf commands, and avoid using the broader workflow automation language as authority for unrelated actions.

Risk: PDF processing may involve sensitive documents, and the evidence does not establish whether nano-pdf or any API sends content off-device.

Mitigation: Use copies of PDFs first, avoid sensitive documents until data handling is understood, and prefer isolated or local processing where available.

Risk: Natural-language PDF edits and page targeting can produce incorrect output.

Mitigation: Review the generated or modified PDF before sharing it and retry with corrected page indexing or clearer instructions when results are off target.

## Reference(s):

- [ClawHub skill page: nano-pdf-2](https://clawhub.ai/thcjp/skills/nano-pdf-2)
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose nano-pdf commands and related configuration; PDF file reads and writes depend on the agent permissions granted by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
