## Description:

Image processing with the oiiotool CLI for format conversion, OCIO/ACES color management, exposure adjustment, resizing and cropping, compositing, EXR sequence video conversion, texture baking, image comparison, and batch image operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oumad](https://clawhub.ai/user/oumad)

### License/Terms of Use:


## Use Case:

Developers, VFX and CGI artists, and pipeline engineers use this skill to produce oiiotool commands and workflow guidance for converting, inspecting, color-managing, comparing, and batch-processing image files and EXR sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image-processing and video commands can overwrite outputs or produce lossy deliverables if paths, codecs, or compression settings are wrong.

Mitigation: Check output paths before running helpers, keep originals, and review lossy compression settings before writing final assets.

Risk: Results can vary across machines when command-line tools or Python packages are installed without pinned versions.

Mitigation: Install in a virtual environment and pin OpenImageIO and Pillow when reproducible output is required.

## Reference(s):

- [OpenImageIO Documentation](https://docs.openimageio.org)
- [ClawHub Oiiotool Skill Page](https://clawhub.ai/oumad/skills/oiiotool)
- [ACES Display Transforms Reference](artifact/references/aces-displays.md)
- [Image Format Reference](artifact/references/formats.md)
- [oiiotool Usage Examples](artifact/references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may depend on local oiiotool, ffmpeg, OpenColorIO, OpenImageIO, and Pillow versions.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
