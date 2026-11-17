## Description:

File format conversion skill. Convert between PDF, DOCX, Markdown, HTML, images, audio, and video formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare file conversion commands for documents, images, audio, and video, including batch conversion, image resizing, and audio extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversion commands write files to user-chosen output paths and may overwrite an existing file if the same output path is reused.

Mitigation: Confirm input and output paths before running commands, and use a fresh output path or back up existing files before conversion.

Risk: The artifact references a converter script that is not included.

Mitigation: Verify that scripts/convert.py or an equivalent converter exists in the execution environment and supports the requested options before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-file-converter)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe input and output paths, target formats, quality settings, resize dimensions, directories, and audio extraction options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
