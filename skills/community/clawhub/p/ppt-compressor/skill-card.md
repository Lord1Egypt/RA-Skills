## Description: <br>
Compresses PPTX presentations by optimizing embedded images and videos, cleaning redundant data, and repackaging the file to reduce size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyifm](https://clawhub.ai/user/liyifm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document owners use this skill to reduce the size of PowerPoint `.pptx` files before sharing, archiving, or uploading them. It is useful when embedded media makes a presentation too large and the user can accept configurable image or video compression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compression can reduce image or video quality and may remove thumbnails, comments, metadata, or other presentation data depending on selected options. <br>
Mitigation: Keep the original presentation, inspect the compressed file before relying on it, and use lower compression or disable PNG conversion, video compression, or comment removal when fidelity matters. <br>
Risk: Video compression depends on an external ffmpeg executable. <br>
Mitigation: Use a trusted ffmpeg installation, or run with video compression disabled when ffmpeg is unavailable or not trusted. <br>


## Reference(s): <br>
- [PPT压缩 on ClawHub](https://clawhub.ai/liyifm/ppt-compressor) <br>
- [ffmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Compressed PPTX file with terminal status output and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a new compressed `.pptx`; optional video compression requires a trusted ffmpeg installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
