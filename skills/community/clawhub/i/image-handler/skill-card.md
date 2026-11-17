## Description:

Read, analyze metadata, convert formats, resize, rotate, crop, compress, and batch process PNG, JPG, GIF, WebP, TIFF, BMP, HEIC, SVG, and ICO images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect image metadata and generate local image-processing commands for format conversion, resizing, rotation, cropping, compression, metadata stripping, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversion and batch commands can create or overwrite image files.

Mitigation: Use explicit output paths and check whether destination files already exist before running commands.

Risk: Untrusted filenames or unusual quality arguments may behave unexpectedly in shell-based image workflows.

Mitigation: Avoid untrusted filenames and unusual quality values until the scripts are hardened.

## Reference(s):

- [Image Handler skill page](https://clawhub.ai/neckr0ik/skills/image-handler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file reads, image conversion commands, and output file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
