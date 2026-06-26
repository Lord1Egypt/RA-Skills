## Description: <br>
Analyze local audio and video files to extract media metadata, audio details, video frame information, covers, and waveform visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and media operators use this skill to inspect selected media files, extract structured metadata, capture representative frames or covers, and generate audio waveform images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated frame, cover, or waveform files can overwrite existing files when the same output path is reused. <br>
Mitigation: Use explicit, unique output filenames or run generation commands in a scratch directory. <br>
Risk: Analysis depends on the local ffmpeg and ffprobe binaries used to process selected media files. <br>
Mitigation: Use trusted ffmpeg and ffprobe installations and process only media files the user intends to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/media-analyze-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands] <br>
**Output Format:** [Command output as structured JSON or status text, with optional generated JPG or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and ffprobe on the local system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
