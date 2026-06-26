## Description: <br>
Image Compress is a cross-platform OpenClaw skill that uses sharp to compress single images or folders, convert image formats, adjust quality, and resize images without overwriting originals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JustZeroX](https://clawhub.ai/user/JustZeroX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to reduce local image file sizes, convert images among JPG, PNG, WebP, AVIF, and HEIC-related formats, resize large images, and prepare images for web pages, email, messaging, or upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Node dependencies for sharp and commander during setup. <br>
Mitigation: Install only in environments where npm dependency installation is acceptable and review the package lock or resolved dependencies before production use. <br>
Risk: Recursive mode can process many files under a selected folder. <br>
Mitigation: Use recursive mode only on intentionally selected folders and confirm the configured output directory before running large batches. <br>
Risk: The scanner guidance notes that large-file warning text is informational because the code does not actually wait for user input before continuing. <br>
Mitigation: Treat large-file warnings as a prompt to stop and rerun with smaller inputs or explicit parameters when processing time or resource use is a concern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JustZeroX/image-compress) <br>
- [Image Compress technical reference](references/technical.md) <br>
- [sharp image processing documentation](https://sharp.pixelplumbing.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Markdown guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes compressed copies under the configured output folder and reports compression results; original images are not overwritten.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
