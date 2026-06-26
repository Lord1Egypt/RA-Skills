## Description: <br>
Adds Feishu/Lark voice interaction using faster-whisper for speech recognition, AI processing for replies, Edge TTS for synthesis, and OPUS conversion for audio responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add voice-based conversations to Feishu/Lark channels, including transcription of incoming audio, AI response generation, and synthesized voice replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact scripts can modify another OpenClaw extension. <br>
Mitigation: Review the shell scripts before installation, avoid running fix-debug-leak.sh unless the QQBot modification is intentional, and keep backups before use. <br>
Risk: Install-time code is unverified. <br>
Mitigation: Run installation only in a controlled environment after script review and verify dependencies before using the skill in production. <br>
Risk: Feishu credentials and sensitive voice or chat data may be exposed through configuration or runtime behavior. <br>
Mitigation: Prefer environment variables over openclaw.json, rotate Feishu credentials, and avoid sensitive voice or chat data until privacy wording and TTS script safety are fixed. <br>
Risk: The default HuggingFace mirror may not be trusted in all environments. <br>
Mitigation: Disable the mirror or set HF_ENDPOINT to a trusted source before downloading models. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-feishu-qq-audio) <br>
- [Publisher profile](https://clawhub.ai/user/43622283) <br>
- [Artifact README (English)](artifact/README_EN.md) <br>
- [Artifact security guide](artifact/SECURITY.md) <br>
- [Artifact security warning](artifact/SECURITY_WARNING.md) <br>
- [Model selection guide](artifact/scripts/MODEL_CHOICE.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Hugging Face](https://huggingface.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and shell commands; runtime scripts emit transcription text and MP3/OPUS audio artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, ffmpeg, jq, uv, Python 3.11+, faster-whisper, and Edge TTS network access.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
