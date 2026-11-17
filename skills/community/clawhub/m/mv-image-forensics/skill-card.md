## Description:

Helps developers compare image softness at matched scale and investigate pixel changes between an original image and a processed delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers reviewing generated or processed images use the skill to compare images at a matched scale and inspect pixel differences against original files. They should verify the source images and actual scaling before relying on comparison labels or conclusions about blur attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comparison labels and conclusions about what caused blur can be unreliable.

Mitigation: Check the original images and actual scaling before relying on labels or attribution; a reproduced resize does not establish that resizing preserved image quality.

Risk: The comparison scripts require three Python dependencies and can overwrite prior results if outputs share a path.

Mitigation: Account for the three dependencies and choose separate output paths for each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catsmansion/skills/mv-image-forensics)

## Skill Output:

**Output Type(s):** [Analysis, Image files, JSON, Guidance]

**Output Format:** [PNG comparison montage, textual or JSON pixel-difference report, and Markdown workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the supplied source and delivered images and the selected comparison settings.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
