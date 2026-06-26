## Description: <br>
Connects OpenClaw agents to mongol.open-idea.net for Chinese, Traditional Mongolian, and Cyrillic Mongolian translation, Mongolian chat and writing, TTS, ASR, OCR, and Word/PDF document translation using the user's API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knixie](https://clawhub.ai/user/knixie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route Mongolian-language translation, generation, speech, OCR, and document tasks through Mongol AI's API while preserving key-handling, routing, and billing-response rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested text, images, audio, and documents to the disclosed mongol.open-idea.net service. <br>
Mitigation: Use it only for content that may be sent to that service, and require confirmation before sensitive OCR, ASR, document-translation, batch, or large jobs. <br>
Risk: The skill requires a paid user API key and can incur charges for successful API calls. <br>
Mitigation: Keep MONGOL_AI_SKILL_API_KEY in OpenClaw configuration, avoid pasting it into chat, and show billing details from response headers or body when available. <br>
Risk: Retrying the same paid request after a successful or partially successful response can duplicate charges. <br>
Mitigation: Do not retry the same content or file after a successful response without explaining the risk and obtaining user confirmation. <br>


## Reference(s): <br>
- [Mongol AI homepage](https://mongol.open-idea.net) <br>
- [HTTP request templates](references/HTTP-REQUESTS.md) <br>
- [Interface routing](references/INTERFACE-ROUTING.md) <br>
- [Translation](references/TRANSLATION.md) <br>
- [Chat completions](references/CHAT-COMPLETIONS.md) <br>
- [OCR](references/OCR.md) <br>
- [ASR](references/ASR.md) <br>
- [TTS](references/TTS.md) <br>
- [Document translation](references/DOCUMENT-TRANSLATION.md) <br>
- [API key setup](references/API-KEY.md) <br>
- [Behavior rules](references/BEHAVIOR-RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with API request examples, final text responses, and optional audio file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful user-facing responses include business content plus a billing line when billing fields are returned; TTS decodes audioBase64 to WAV instead of displaying raw audio data.] <br>

## Skill Version(s): <br>
1.0.36 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
