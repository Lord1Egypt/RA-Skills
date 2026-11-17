## Description:

会议纪要与会议播报生成技能。用于处理会议录音或转写文本，执行发言人区分、口语降噪、议题重构、双钻结构整理，并输出执行摘要、核心决议、Markdown待办表格、TTS播报稿和会议思维导图（HTML/SVG/XMind）。支持双向语音能力：录音转文本（ASR）与文本转录音（TTS）。用户提到“会议纪要”“录音转文字”“文字转语音”“action items”“会后总结”“决议整理”“语音简报/会议播客”“思维导图/脑图”时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2813223285](https://clawhub.ai/user/2813223285)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external meeting participants use this skill to turn meeting recordings, transcripts, or raw notes into structured Chinese meeting minutes, action items, a short speech brief, and a visual mind map. It is suited for meeting follow-up workflows that need concise decisions, owners, dates, risks, and shareable deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the local environment by installing or requiring packages such as edge-tts, ffmpeg, and openai-whisper.

Mitigation: Review installation steps before first use, pin approved dependency versions where required, and run the dependency doctor in a controlled environment.

Risk: Meeting recordings or text may be sent to cloud speech providers when fallback providers are used.

Mitigation: Use a local-only provider policy for confidential meetings and require explicit approval before enabling cloud ASR or TTS providers.

Risk: Generated meeting files can persist sensitive meeting content on disk.

Mitigation: Use the private output directory, define retention and deletion procedures, and avoid quick-copy behavior for confidential material.

Risk: Generated HTML mind maps may contain unsafe or insufficiently escaped meeting content.

Mitigation: Review generated HTML before sharing and restrict use to trusted viewers until escaping and sanitization controls are validated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2813223285/skills/meeting-notes-skill)
- [Publisher Profile](https://clawhub.ai/user/2813223285)
- [Output Template](references/output-template.md)
- [Quality Gate Checklist](references/quality-gate-checklist.md)
- [Homebrew](https://brew.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown plus generated text, MP3 audio, HTML/SVG/XMind mind-map files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default final deliverables are a minutes text file, a brief MP3 audio file, and an HTML mind map with a shared meeting-topic timestamp prefix.]

## Skill Version(s):

1.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
