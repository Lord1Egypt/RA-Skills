## Description:

Personalized news radio generation skill for creating topic-based audio briefings, configuring TTS voices, scheduling daily delivery, and reviewing generated radio history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayden-x-l](https://clawhub.ai/user/jayden-x-l)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw or LobsterAI cowork mode to turn platform-LLM-generated news or topic text into local Qwen3-TTS audio briefings. It also supports voice configuration, scheduled delivery setup, and access to generated radio history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use network access and download large ML models.

Mitigation: Install in a virtual environment and review model sources before enabling trust_remote_code examples or automatic downloads.

Risk: The skill saves generated audio files locally and writes TTS or user configuration into OpenClaw memory.

Mitigation: Back up ~/.openclaw/MEMORY.md and generated radio data, and review storage locations and file permissions before deployment.

Risk: Scheduled task setup can repeatedly generate or push audio content.

Mitigation: Review schedule frequency, delivery channel, and recipient configuration before enabling automated delivery.

Risk: Filename and TTS configuration fields may receive untrusted input before validation is added.

Mitigation: Avoid passing untrusted values for filenames, paths, voice IDs, and TTS settings until input validation is confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayden-x-l/skills/lobster-radio-skill)
- [Qwen3-TTS Hugging Face Model](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice)
- [Qwen3-TTS ModelScope Model](https://modelscope.cn/models/qwen/Qwen3-TTS-12Hz-0.6B-Base)
- [Qwen3-TTS Repository](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS Blog](https://qwen.ai/blog?id=qwen3tts-0115)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [LobsterAI Repository](https://github.com/netease-youdao/LobsterAI)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown or text responses with audio file links, configuration guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated audio files locally and return relative or absolute file paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
