## Description:

Fill PDF forms programmatically with text values and checkboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raulsimpetru](https://clawhub.ai/user/raulsimpetru)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to discover fields in fillable PDFs and generate completed PDF files from supplied text and checkbox data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes PDF output files and may overwrite an existing destination path if the caller chooses one.

Mitigation: Write outputs to new filenames or a dedicated output directory, as recommended by the security guidance.

Risk: The skill processes local PDF and data files supplied by the user.

Mitigation: Use it only on PDFs and data files the user intends to process.

Risk: The skill depends on pdfrw for PDF parsing and writing.

Mitigation: Review or pin the pdfrw dependency before installing in sensitive environments.

## Reference(s):

- [PDF Form Filler Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/raulsimpetru/skills/pdf-form-filler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and generated PDF files when executed by the user or agent environment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reads user-specified PDF and JSON inputs and writes filled PDF outputs.]

## Skill Version(s):

0.2.0 (source: frontmatter, package metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
