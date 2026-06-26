## Description: <br>
Kokoro TTS generates spoken audio from text using a local or configured Kokoro TTS engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edkief](https://clawhub.ai/user/edkief) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to convert requested text into MP3 speech output through a Kokoro TTS endpoint for OpenClaw audio attachment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is sent to the configured Kokoro API endpoint. <br>
Mitigation: Use a trusted Kokoro endpoint, prefer the localhost default when possible, and avoid sending secrets or sensitive private text to untrusted remote servers. <br>
Risk: Generated audio files can accumulate in the local media directory. <br>
Mitigation: Review and clean the media directory periodically according to the workspace's retention needs. <br>


## Reference(s): <br>
- [Available Kokoro Voices](references/voices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text command guidance and MEDIA-prefixed MP3 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated MP3 audio files to the local media directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
