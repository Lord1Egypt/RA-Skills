## Description: <br>
PixelMagic-PhotoLogic-9z helps agents edit and batch-process photos locally with ImageMagick presets for styles such as cinematic apocalyptic, fresh Japanese, vintage film, and high-contrast black-and-white looks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[couplefishes](https://clawhub.ai/user/couplefishes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to retouch, color-grade, filter, and batch-process RAW, JPG, PNG, and TIFF photos while preserving originals and final output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local ImageMagick commands and may suggest package-manager installation commands. <br>
Mitigation: Review installation commands before running them and keep ImageMagick updated. <br>
Risk: Photo processing can leave originals, intermediate files, logs, parameters, and final derivatives in a local work directory. <br>
Mitigation: Process sensitive photos only in a directory you control and delete the generated work folder when retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/couplefishes/pixelmagic-photologic-9z) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus local image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local image-editor-work directory with originals, intermediate files when retained, logs, parameter records, and final edited images.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
