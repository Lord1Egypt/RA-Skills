## Description:

Convert Markdown (.md) files to Word (.docx), PDF, and styled HTML in one shot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelley99](https://clawhub.ai/user/kelley99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert Markdown files into shareable Word, PDF, or styled HTML documents, including documents with Chinese text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML conversion of untrusted Markdown may preserve unsafe raw HTML or script content.

Mitigation: Do not use the HTML converter on untrusted Markdown unless the output is sanitized or raw HTML and script content are disabled.

Risk: Unpinned Python dependencies can change behavior across environments.

Mitigation: Install dependencies in a normal user environment or virtual environment, and prefer pinned dependency versions when maintaining the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HTML, DOCX, PDF, or all three from a Markdown input; DOCX and PDF conversion require Python dependencies.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
