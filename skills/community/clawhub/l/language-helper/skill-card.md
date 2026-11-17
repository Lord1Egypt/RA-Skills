## Description:

Language Helper translates language-learning prompts, generates SenseAudio pronunciation audio, and returns grammar and vocabulary guidance for supported target languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igloomatics](https://clawhub.ai/user/igloomatics)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to ask how to say a phrase in another language, hear generated pronunciation audio, and receive concise grammar, vocabulary, and alternative-expression guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pronunciation audio can be uploaded and sent to configured Feishu chats without per-use confirmation.

Mitigation: Enable Feishu delivery only when needed, use a narrowly scoped bot, configure a deliberate chat ID, and avoid sending private phrases to shared chats.

Risk: Sensitive text or credentials can be exposed if .env files or debug logs are mishandled.

Mitigation: Store credentials in environment variables or a locked-down .env file, do not commit .env or logs, and avoid debug logging for sensitive phrases.

## Reference(s):

- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2)
- [SenseAudio](https://senseaudio.cn)
- [Feishu app console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, audio files, guidance]

**Output Format:** [Markdown with translation text, pronunciation notes, vocabulary tables, inline shell commands, and optional generated audio.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can fall back to text-only guidance when TTS is unavailable; optional Feishu delivery sends generated voice messages to a configured chat.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
