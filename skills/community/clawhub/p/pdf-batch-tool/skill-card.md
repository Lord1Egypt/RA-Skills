## Description:

Batch process PDF files by merging, splitting, converting to images, extracting text, adding watermarks, and compressing documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity-focused users can use this skill to guide batch PDF workflows such as combining files, extracting pages or text, converting pages to PNG or JPG images, applying text watermarks, and compressing PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example output paths could overwrite existing files or directories if reused without checking the workspace.

Mitigation: Choose explicit output paths, prefer new directories for generated images, and confirm overwrite behavior before running file operations.

Risk: The skill instructions are primarily in Chinese, which can lead to incorrect parameter use for readers who are not comfortable with the language.

Mitigation: Confirm command intent and parameters before execution, especially page ranges, quality settings, watermark text, and output destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/pdf-batch-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown with command examples and file path parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify PDF, PNG, JPG, and TXT files when the agent carries out the described PDF operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
