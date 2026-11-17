## Description:

Expert Pillow (PIL) skill for image processing, manipulation, and analysis, including image editing, batch processing, watermarking, format conversion, and extracting image information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangruihan](https://clawhub.ai/user/yangruihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate common 2D image workflows such as resizing, cropping, rotating, color adjustment, batch conversion, watermarking, and metadata inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image edits and batch processing write output files and can overwrite important work if paths are chosen carelessly.

Mitigation: Use separate output directories, keep backups of originals, and verify paths before running helper scripts.

Risk: EXIF and JSON metadata outputs can expose private information from source images.

Mitigation: Review metadata before sharing outputs and avoid publishing EXIF or generated JSON files that contain sensitive fields.

Risk: Unpinned dependencies and unused packages can increase maintenance and supply-chain review burden.

Mitigation: Install in a dedicated virtual environment, pin or review dependency versions, and remove openpyxl if it is not needed.

Risk: Very large or untrusted images and extreme worker settings can consume significant memory or CPU.

Mitigation: Avoid untrusted oversized images, test on a small sample first, and use conservative batch sizes and worker counts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangruihan/skills/image-edit-skill)
- [Pillow common operations reference](references/common_operations.md)
- [Image processing best practices](references/best_practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional text or JSON metadata output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image files and metadata files when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
