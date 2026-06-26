## Description: <br>
Recover working OpenClaw Telegram voice messaging after upgrades or rebuilds by restoring the local faster-whisper transcription helper, keeping native inbound/outbound voice routing, and applying the Microsoft TTS provider configuration fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenredmond-straiteis](https://clawhub.ai/user/stephenredmond-straiteis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to recover OpenClaw Telegram voice-note transcription and outbound voice replies after upgrades or rebuilds. It focuses on local helper runtime restoration and the Microsoft TTS/OpenClaw configuration needed when inbound transcription works but outbound audio replies fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TTS reply text may be sent to Microsoft/Edge TTS despite offline/local framing. <br>
Mitigation: Review and accept hosted TTS handling before installation, and avoid sending sensitive reply text through the TTS path unless that is permitted. <br>
Risk: Generated audio may remain cached under ~/.openclaw/tts. <br>
Mitigation: Treat the cache directory as containing potentially sensitive audio and clear or protect it according to local retention requirements. <br>
Risk: Audio path handling includes an unsafe shell=True ffmpeg call. <br>
Mitigation: Patch the ffmpeg invocation before processing untrusted Telegram or OpenClaw media paths. <br>
Risk: The installer pulls dependencies and expects a transcribe-audio helper that is absent from the artifact file list. <br>
Mitigation: Pin or vet dependencies before deployment and confirm the transcribe-audio helper is supplied in the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stephenredmond-straiteis/lessac-offline-voice-system) <br>
- [Recovery Notes](references/recovery-notes.md) <br>
- [Voice Models Reference](references/voice_models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce installation, restart, testing, and OpenClaw configuration guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
