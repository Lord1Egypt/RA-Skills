## Description: <br>
Analyze media file properties - duration, resolution, bitrate, codecs, and stream information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media engineers use this skill to inspect audio and video files with ffmpeg and ffprobe, including duration, resolution, bitrate, codecs, stream counts, frame rate, sample rate, and channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ffmpeg and ffprobe parse complex media formats, so untrusted or sensitive media files can create security and privacy exposure during inspection. <br>
Mitigation: Use trusted ffmpeg and ffprobe builds, inspect only media files you choose, and apply normal handling controls for sensitive or untrusted files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples and ffprobe JSON output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on user-selected local media files and may produce plain text, CSV, or JSON metadata output depending on the ffprobe flags used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
