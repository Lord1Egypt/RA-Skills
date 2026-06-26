## Description: <br>
Image processing with the oiiotool CLI for format conversion, OCIO/ACES color management, exposure adjustment, resizing and cropping, compositing, EXR sequence-to-video workflows, texture baking, image comparison, and batch or sequence operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oumad](https://clawhub.ai/user/oumad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, VFX artists, CGI teams, game developers, and photography workflows use this skill to generate oiiotool, OpenColorIO, and ffmpeg commands for local image processing, HDR review, color transforms, sequence conversion, and inspection tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and helper scripts can overwrite output files when paths point at existing assets. <br>
Mitigation: Use explicit output directories, avoid important existing files as outputs, and review target paths before running commands. <br>
Risk: Metadata manipulation commands can alter or remove image metadata. <br>
Mitigation: Review metadata commands before execution and keep source files or backups when metadata must be preserved. <br>
Risk: The workflow depends on local OpenImageIO, oiiotool, ffmpeg, and Python tooling. <br>
Mitigation: Install required tools from trusted sources and verify local binaries before using the generated commands. <br>


## Reference(s): <br>
- [OpenImageIO Documentation](https://docs.openimageio.org) <br>
- [ACES Display Transforms Reference](references/aces-displays.md) <br>
- [Format Reference](references/formats.md) <br>
- [Usage Examples](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, command options, color-space names, format settings, and helper-script invocations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
