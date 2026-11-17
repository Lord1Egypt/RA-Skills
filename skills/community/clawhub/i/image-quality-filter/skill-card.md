## Description:

Detects low-quality images by analyzing blur, brightness, and resolution so agents can help clean image datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and dataset maintainers use this skill to scan image folders, identify blurry, underexposed, overexposed, or low-resolution files, and choose whether to list, move, or delete low-quality images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk delete or move actions can remove original images or important dataset files.

Mitigation: Run the default list action first, review reported images, and keep backups before using delete or move.

Risk: Moving low-quality images into a destination that already contains same-named files may overwrite data.

Mitigation: Use a new or empty output directory for move actions and test on a small sample before processing a full dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingo-318/skills/image-quality-filter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include threshold recommendations, scan commands, and cautions for file-moving or deletion workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
