## Description:

Use this skill whenever the user wants to convert text into speech, generate audio from text, or produce voiceovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksuriuri](https://clawhub.ai/user/ksuriuri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and workflow agents use this skill to generate speech audio, voiceovers, subtitle-aligned narration, and voice-mapped dubbing from text, documents, or SRT timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, subtitles, and voice-reference audio may be sent to Noiz unless the local Kokoro backend is explicitly selected.

Mitigation: Use Kokoro for sensitive content, and install or run the skill only when Noiz cloud processing is acceptable for the data involved.

Risk: Untrusted base URLs, reference-audio URLs, or workflow-supplied arguments can create credential and data exposure paths.

Mitigation: Allow only trusted command arguments and URLs, keep NOIZ_API_KEY in a managed secret or environment variable, and rotate the key if untrusted inputs may have influenced execution.

Risk: Temporary render files may retain sensitive text or audio after timeline processing.

Mitigation: Clear .tmp/tts after sensitive renders and review generated output paths before sharing artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksuriuri/skills/noizai-tts)
- [Third-Party Voice Delivery Reference](artifact/ref_3rd_party.md)
- [Noiz Developer API Keys](https://developers.noiz.ai/api-keys)
- [Noiz API endpoint](https://noiz.ai/v1/)
- [Feishu upload file API](https://open.feishu.cn/document/server-docs/im-v1/file/create)
- [Feishu send message API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [Telegram sendVoice API](https://core.telegram.org/bots/api#sendvoice)
- [Discord uploading files API](https://discord.com/developers/docs/reference#uploading-files)
- [Discord create message API](https://discord.com/developers/docs/resources/channel#create-message)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON voice-map examples, configuration guidance, and generated audio or subtitle files when commands are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce audio files, SRT files, temporary render artifacts, and Noiz API calls depending on backend and options.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
