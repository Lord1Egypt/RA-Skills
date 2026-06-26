## Description: <br>
Media Processor helps agents download, compress, watermark, and convert local or remote images and videos, including MP4 and m3u8 streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobai-6543](https://clawhub.ai/user/mobai-6543) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare media for publishing or downstream workflows by compressing assets, adding text watermarks, and converting video to H.264-compatible output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote media handling can fetch untrusted or private/internal URLs when the agent is given a URL. <br>
Mitigation: Install and run it only where downloading and processing remote media is acceptable, and avoid private/internal or untrusted URLs. <br>
Risk: Media processing depends on FFmpeg and Python packages that require routine security maintenance. <br>
Mitigation: Use a virtual environment or container and keep FFmpeg and Python dependencies updated. <br>
Risk: Processed files are written to user-provided or default output paths. <br>
Mitigation: Choose output paths deliberately and review generated files before relying on them to avoid overwriting important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobai-6543/media-processor-agent) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Processed image or video files with status text and output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes processed media to the requested output path, or to a default local media path when no output is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
