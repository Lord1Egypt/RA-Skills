## Description:

Generate professional PDF documents from structured JSON data, including styled titles, tables, lists, highlights, images, and page breaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexrox](https://clawhub.ai/user/flexrox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert structured report data into a local PDF file with headings, tables, lists, callouts, images, and page breaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script writes a PDF to the path supplied by the user or JSON data.

Mitigation: Review the output path before running the skill and avoid writing into sensitive or unintended locations.

Risk: The script reads JSON files and image paths supplied in the input data.

Mitigation: Use trusted local input files and confirm referenced image paths before execution.

Risk: Built-in author and date labels appear in German.

Mitigation: Account for the localized labels in generated documents or update the skill before using it for audiences that require another language.

## Reference(s):

- [PDF Generator Schema Reference](references/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/flexrox/skills/pragdev-pdf-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; the skill's script writes PDF files to the requested output path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON input with optional title, subtitle, author, date, colors, style overrides, sections, image paths, and output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
