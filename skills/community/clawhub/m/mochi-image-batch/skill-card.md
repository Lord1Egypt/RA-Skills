## Description:

Batch resize, crop, pad, compress, convert and watermark images, with contact sheets and downloadable results. Use for Batch Image Processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and content teams can batch-process workspace images for resizing, cropping, padding, compression, format conversion, and watermarking, then review a contact sheet and download the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports and SHA256 receipts remain in the workspace until removed.

Mitigation: Review the generated files and remove exports and receipts when they are no longer needed.

Risk: A strict byte limit can reduce output image dimensions.

Mitigation: Check manifest.json and confirm the final dimensions meet the intended use.

Risk: The image-processing environment depends on Python and Pillow versions.

Mitigation: Use a dedicated Python environment and review installer and dependency versions.

## Reference(s):

- [Image processing input contract](references/input.md)
- [MochiLab](https://mochilab.bz)
- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-image-batch)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JPEG, PNG, or WebP images, a JPEG contact sheet, a JSON manifest, and a ZIP archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 200 images per job; originals are retained and output image metadata is stripped.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
