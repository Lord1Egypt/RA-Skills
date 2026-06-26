## Description: <br>
Enables agents to synthesize speech, clone and design voices, and post-process audio using the MiniMax Voice API and FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BLUE-coconut](https://clawhub.ai/user/BLUE-coconut) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to convert text into speech, prepare multi-voice segment plans, create or manage custom voices, and run audio processing workflows with MiniMax and FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, prompts, and voice recordings may be sent to MiniMax under the user's API key. <br>
Mitigation: Use the skill only with content and recordings the user is comfortable sending to MiniMax, and avoid including secrets in prompt or preview text. <br>
Risk: Voice cloning can process recordings containing personal or third-party voice data. <br>
Mitigation: Use voice cloning only with recordings the user owns or has explicit permission to process. <br>
Risk: Cloud custom voice assets may be deleted by cleanup_unused_voices(dry_run=False). <br>
Mitigation: Run destructive cleanup only when the user intends to delete all custom cloned or designed voices in the account. <br>
Risk: API keys could be exposed during setup or troubleshooting. <br>
Mitigation: Do not echo, screenshot, or include API keys in shared prompts, logs, or preview text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BLUE-coconut/mm-voice-maker) <br>
- [MiniMax Voice API base URL](https://api.minimaxi.com/v1) <br>
- [Command Line Interface Guide](reference/cli-guide.md) <br>
- [Getting Started](reference/getting-started.md) <br>
- [Text-to-Speech Guide](reference/tts-guide.md) <br>
- [Voice Creation Guide](reference/voice-guide.md) <br>
- [Audio Processing Guide](reference/audio-guide.md) <br>
- [MiniMax Voice Catalog](reference/voice-catalog.md) <br>
- [MiniMax Voice API Complete Reference](reference/api_documentation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON segment plans, Python examples, shell commands, and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local segments.json, preview audio, merged audio outputs, and processed audio files when the referenced CLI or scripts are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
