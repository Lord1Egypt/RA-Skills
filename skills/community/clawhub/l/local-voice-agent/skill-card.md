## Description: <br>
Complete offline voice-to-voice AI assistant for OpenClaw (Whisper.cpp STT + Pocket-TTS). 100% local processing, no cloud APIs, no costs. Use for hands-free operation, voice commands, accessibility, or custom voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinological](https://clawhub.ai/user/pinological) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add local speech-to-text, AI response handling, and text-to-speech workflows for hands-free commands, accessibility, voice notes, and conversational operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads microphone or audio-file input and can create transcripts, generated speech, cache files, temporary files, or logs that may contain private information. <br>
Mitigation: Review cache and logging settings before use, disable caching for sensitive content, and clear local transcript or audio artifacts when they are no longer needed. <br>
Risk: Generated text is sent to the configured TTS server, and privacy depends on where that server is hosted. <br>
Mitigation: Keep the TTS URL set to localhost unless a remote server is explicitly trusted and approved for the data being spoken. <br>
Risk: Exposing Pocket-TTS on a broad network interface can make generated voice services reachable outside the local machine. <br>
Mitigation: Bind Pocket-TTS to localhost for normal use and avoid 0.0.0.0 unless network access is intentional and access controls are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pinological/local-voice-agent) <br>
- [Whisper.cpp repository](https://github.com/ggerganov/whisper.cpp) <br>
- [Pocket-TTS repository](https://github.com/kyutai-labs/pocket-tts) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local transcript, cache, log, and generated audio files when the installed scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
