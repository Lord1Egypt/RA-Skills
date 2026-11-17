## Description:

Uses Pillow to convert among common image formats including PNG, JPEG, GIF, BMP, TIFF, and WebP, with same-format compression, quality controls, resizing, and lossless modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanocifer](https://clawhub.ai/user/kanocifer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare local image assets by converting files or directories between common formats, compressing images, resizing by maximum edge length, and controlling lossy or lossless output settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversion writes files to user-specified output paths, so careless path selection can create or overwrite files outside the intended location.

Mitigation: Review input and output paths before execution and use a dedicated output directory for converted assets.

Risk: Directory conversion can increase disk usage unexpectedly if the output directory is placed inside the input directory.

Mitigation: Choose an output directory outside the input tree when converting directories.

Risk: Unpinned Pillow installations can change conversion behavior across environments.

Mitigation: Install Pillow in a virtual environment and consider pinning the dependency version.

## Reference(s):

- [WebP settings reference](artifact/references/webp_settings.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples and local Python script usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local image output files when the conversion script is run; no network services or API calls are required by the artifact.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
