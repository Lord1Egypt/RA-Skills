## Description:

Li Feishu Audio enables Feishu voice-message workflows by transcribing user audio with faster-whisper, passing recognized text to an AI reply flow, synthesizing speech with Edge TTS, converting audio to OPUS, and sending voice replies through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu voice interaction: receive voice messages, transcribe Chinese audio, generate AI text replies, synthesize spoken responses, and send audio replies back through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts may expose unsafe code-execution behavior, especially when untrusted text is passed into generated Python or shell contexts.

Mitigation: Review or fix the scripts before installation, avoid pasting untrusted content into shell scripts, and replace heredoc-generated Python with fixed modules that receive text and paths as data.

Risk: Feishu credentials may be exposed or over-privileged.

Mitigation: Run without privileged accounts, keep FEISHU_APP_ID and FEISHU_APP_SECRET tightly scoped, redact appSecret output, and rotate credentials regularly.

Risk: Dependency and model downloads may change over time or come from mirrors without pinned revisions.

Mitigation: Pin dependencies and model revisions, and review download sources before deployment.

Risk: Temporary audio files and cleanup paths may expose data or remove unintended files.

Mitigation: Use a private TEMP_DIR and review cleanup behavior before enabling scheduled cleanup.

## Reference(s):

- [README_EN.md](artifact/README_EN.md)
- [SECURITY.md](artifact/SECURITY.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [HuggingFace Mirror](https://hf-mirror.com/)
- [Microsoft Edge TTS service endpoint](https://speech.platform.bing.com/)

## Skill Output:

**Output Type(s):** [Text, Audio files, API calls, Shell commands, Configuration instructions]

**Output Format:** [Recognized text, MP3/OPUS audio files, Feishu audio messages, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; uses configurable model, virtual environment, temporary, OpenClaw configuration, and log paths.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
