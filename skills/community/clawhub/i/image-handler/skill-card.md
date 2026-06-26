## Description: <br>
Read, analyze, convert, and manipulate image files (PNG, JPG, GIF, WebP, TIFF, BMP, HEIC, SVG, ICO). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect image metadata, convert image formats, resize, rotate, crop, compress, strip metadata, and batch process local image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image conversion and batch processing can overwrite or create local files at selected paths. <br>
Mitigation: Confirm input and output paths before running commands and keep originals when converting, resizing, or stripping metadata. <br>
Risk: Image metadata can contain private location, device, or author information. <br>
Mitigation: Review metadata before sharing images and use the documented metadata-stripping workflow when privacy is required. <br>
Risk: Generated shell commands can behave differently depending on local tool availability and image format support. <br>
Mitigation: Review commands before execution and verify that required local tools such as sips or ffmpeg are available for the requested format. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/image-handler) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown with inline bash commands and generated local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input and output paths; conversions may preserve, transform, or strip image metadata depending on the selected command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
