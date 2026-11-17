## Description:

Image Optimizer Tool helps agents guide users through batch image resizing, compression, and format conversion with preview and undo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and other external users use this skill to prepare local image optimization commands for batch resizing, quality compression, format conversion, previewing, and undo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image operations can overwrite or modify local image files when no output directory is used.

Mitigation: Run preview mode first or set --output-dir to write optimized copies before replacing originals.

Risk: The installer uses an unpinned Pillow dependency.

Mitigation: Install in a virtual environment and pin or review the Pillow version before use.

Risk: Backup path handling has a known bug when targeting images outside the current working directory.

Mitigation: Run the tool from the directory being processed or use --output-dir until backup path handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/image-optimizer-tool)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local file paths, quality settings, image dimensions, output formats, preview mode, undo mode, and output-directory settings.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, image_optimizer.py VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
