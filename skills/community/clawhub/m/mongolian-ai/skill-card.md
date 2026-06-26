## Description: <br>
Provides Mongolian language translation, chat and writing support, TTS, ASR, OCR, and Word/PDF document translation through the mongol.open-idea.net service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youteacherasia](https://clawhub.ai/user/youteacherasia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate between Chinese, traditional Mongolian, and Cyrillic Mongolian, create or answer in Mongolian, transcribe or synthesize speech, run OCR, and translate Word or PDF documents. It is useful when an agent needs to route Mongolian-language tasks to a dedicated external API while returning only the requested result and any billing line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, documents, images, and audio selected for processing are sent to mongol.open-idea.net. <br>
Mitigation: Use the skill only for content you are allowed to send to that service, and avoid sensitive, confidential, or regulated information. <br>
Risk: The skill requires a user API key and may incur charges for successful requests. <br>
Mitigation: Store MONGOL_AI_SKILL_API_KEY in the local environment, do not paste keys into chat, and confirm large, batch, document, OCR, or long audio jobs before submitting them. <br>
Risk: OCR, ASR, TTS, and document workflows handle files whose contents may be larger or more sensitive than a short text prompt. <br>
Mitigation: Review files before upload, keep TTS audio as a file rather than exposing raw audioBase64 or binary content, and avoid blind retries after successful or billable responses. <br>
Risk: Mixed traditional Mongolian and Cyrillic inputs can be routed incorrectly. <br>
Mitigation: Follow the documented routing rules and explicitly choose the OCR or translation script when the content may be Cyrillic or mixed-language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youteacherasia/mongolian-ai) <br>
- [Mongol AI homepage](https://mongol.open-idea.net) <br>
- [API key setup](references/API-KEY.md) <br>
- [Behavior rules](references/BEHAVIOR-RULES.md) <br>
- [HTTP request templates](references/HTTP-REQUESTS.md) <br>
- [Interface routing](references/INTERFACE-ROUTING.md) <br>
- [Translation reference](references/TRANSLATION.md) <br>
- [Chat completions reference](references/CHAT-COMPLETIONS.md) <br>
- [OCR reference](references/OCR.md) <br>
- [ASR reference](references/ASR.md) <br>
- [TTS reference](references/TTS.md) <br>
- [Document translation reference](references/DOCUMENT-TRANSLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses with translated text, recognized text, transcriptions, billing lines, configuration commands, and local audio or document file references when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONGOL_AI_SKILL_API_KEY and sends selected text, files, images, or audio to mongol.open-idea.net; TTS may produce local WAV audio rather than pasted binary content.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
