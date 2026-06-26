## Description: <br>
Switch OpenClaw ElevenLabs TTS voices by updating ~/.openclaw/openclaw.json, keeping Chinese-safe defaults, and restarting the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NowLoadY](https://clawhub.ai/user/NowLoadY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to change the ElevenLabs voice used by OpenClaw Gateway built-in TTS, while preserving safe defaults for Chinese language output and multilingual model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit local OpenClaw TTS configuration and restart the OpenClaw Gateway. <br>
Mitigation: Review the target voice, language, and model before running the switch script, and keep the generated backup available for rollback. <br>
Risk: The voice-listing workflow may use an ElevenLabs API key from configuration or environment variables. <br>
Mitigation: Prefer an existing config entry or protected environment variable, and avoid pasting secrets into chat or command arguments. <br>


## Reference(s): <br>
- [TTS Parameters](references/tts-parameters.md) <br>
- [ClawHub skill page](https://clawhub.ai/NowLoadY/openclaw-tts-voice-switch) <br>
- [ElevenLabs voices API](https://api.elevenlabs.io/v1/voices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json, create a backup, and restart OpenClaw Gateway when its bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
