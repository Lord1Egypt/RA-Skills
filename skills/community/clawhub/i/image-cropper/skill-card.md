## Description:

Crop objects from images using bounding box annotations in COCO, YOLO, VOC, or LabelMe formats with optional padding and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and dataset maintainers use this skill to crop annotated object regions from image datasets for inspection, training-data preparation, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: COCO annotations can reference image files outside the intended image directory when the annotation file is crafted.

Mitigation: Use trusted annotation files or run the skill in a sandbox with filesystem access limited to the intended image dataset.

Risk: Generated crops are written into the selected output directory and may collide with files the user wants to preserve.

Mitigation: Use a fresh output directory for each run and avoid reusing directories that contain important files.

Risk: Image parsing depends on the local Pillow installation and the input files supplied by the user.

Mitigation: Prefer a pinned Pillow version in the execution environment and process only trusted image datasets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mingo-318/skills/image-cropper)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with inline bash commands; the cropper script writes cropped image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports COCO, YOLO, VOC, and LabelMe-style workflows with options for padding, per-object output, minimum crop size, image format, and JPEG quality.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
