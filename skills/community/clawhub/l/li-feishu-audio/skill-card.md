## Description: <br>
Feishu (Lark) voice interaction skill for automatic voice recognition, AI processing, text-to-speech synthesis, OPUS conversion, and voice replies through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add Feishu voice-message workflows that transcribe incoming audio, generate an AI response, synthesize speech, and send a voice reply back through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure through Feishu app secrets or local environment files. <br>
Mitigation: Use a minimally privileged Feishu app, restrict .env write access to trusted users, rotate credentials regularly, and review scripts before installation. <br>
Risk: Sensitive conversation content may be exposed through raw message, transcript, or configuration logging. <br>
Mitigation: Restrict the bot to approved chats or users and avoid sensitive production conversations until logging and config disclosure behavior is fixed. <br>
Risk: Temporary audio cleanup can remove unintended files if TEMP_DIR is unsafe or misconfigured. <br>
Mitigation: Validate TEMP_DIR before running cleanup manually or through cron, and keep cleanup scoped to the skill's temporary audio directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/43622283/li-feishu-audio) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [HuggingFace mirror](https://hf-mirror.com/) <br>
- [Microsoft Edge TTS endpoint](https://speech.platform.bing.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, audio files, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce transcript text, MP3/OPUS audio files, and Feishu API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; uses faster-whisper, Edge TTS, ffmpeg, jq, uv, and network access to Feishu, HuggingFace mirror, and Microsoft speech services.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
