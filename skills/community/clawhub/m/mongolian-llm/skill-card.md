## Description:

Provides Mongolian-language translation across Chinese, Traditional Mongolian, and Cyrillic Mongolian, plus Mongolian chat, writing, text-to-speech, speech recognition, OCR, and Word/PDF document translation through the Mongol AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knixie](https://clawhub.ai/user/knixie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route Mongolian translation, conversation, OCR, ASR, TTS, and document translation requests to Mongol AI while preserving API-key handling, billing disclosure, and endpoint-specific output rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text, files, images, or audio may be sent to the third-party Mongol AI service.

Mitigation: Use the skill on non-sensitive content unless the user trusts that service and accepts its handling of submitted data.

Risk: The skill uses a paid API under the user's own API key and billing account.

Mitigation: Follow the skill's confirmation and billing-output rules for long, batch, file, OCR, or audio requests, and report only billing fields returned by successful responses.

Risk: API keys could be exposed if pasted into chat or echoed in logs.

Mitigation: Keep MONGOL_AI_SKILL_API_KEY in local OpenClaw configuration and avoid asking users to paste keys into the conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knixie/skills/mongolian-llm)
- [Publisher profile](https://clawhub.ai/user/knixie)
- [Mongol AI homepage](https://mongol.open-idea.net)
- [API Key](references/API-KEY.md)
- [HTTP Requests](references/HTTP-REQUESTS.md)
- [Interface Routing](references/INTERFACE-ROUTING.md)
- [Translation](references/TRANSLATION.md)
- [Chat Completions](references/CHAT-COMPLETIONS.md)
- [OCR](references/OCR.md)
- [ASR](references/ASR.md)
- [TTS](references/TTS.md)
- [Document Translation](references/DOCUMENT-TRANSLATION.md)
- [Behavior Rules](references/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls, audio files]

**Output Format:** [Markdown text with endpoint-specific response fields, billing lines, JSON or curl examples, and decoded WAV output for TTS when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONGOL_AI_SKILL_API_KEY and may send user text, files, images, or audio to mongol.open-idea.net under the user's account.]

## Skill Version(s):

1.0.36 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
