## Description: <br>
Generates Feishu-native voice replies by synthesizing text with Edge TTS, converting the audio to Ogg/Opus with ffmpeg, and sending it as a playable Feishu voice message alongside visible text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to respond in Feishu with both readable text and a native voice bubble when a user asks for spoken playback, a voice reply, or a compact spoken summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text is sent through Edge TTS and may include sensitive content if the agent uses it indiscriminately. <br>
Mitigation: Use the skill only for content that is acceptable to synthesize through Edge TTS; avoid secrets, regulated data, and sensitive internal content. <br>
Risk: Generated MP3 and Ogg/Opus audio files remain in the workspace after voice generation. <br>
Mitigation: Store generated files only in an approved workspace location and apply local retention or cleanup controls appropriate for the content. <br>
Risk: The artifact contains unresolved merge-conflict markers in the skill documentation. <br>
Mitigation: Have the publisher remove the conflict markers before relying on the release documentation operationally. <br>
Risk: The skill depends on local media tooling such as edge-tts, ffmpeg, and optionally ffprobe. <br>
Mitigation: Confirm those dependencies are installed and trusted in the agent runtime before enabling the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeffli-feishu-voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output; generated media files are MP3 and Ogg/Opus.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates workspace-local audio files intended for Feishu voice-message delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
