## Description:

Mongolian AI for Codex routes Mongolian translation, script conversion, chat, OCR, ASR, TTS, and Word/PDF translation tasks through the Mongol AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to handle Traditional and Cyrillic Mongolian language workflows, including translation, conversation, OCR, speech recognition, speech synthesis, and document translation. It is intended for agent workflows that should call the Mongol AI service instead of relying on general model knowledge for Mongolian-language results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested text, images, audio, and documents are sent to the external Mongol AI service for processing.

Mitigation: Use the skill only for content approved for upload, and obtain explicit confirmation before sending confidential, regulated, personal, unexpectedly large, or file-based inputs with unclear sensitivity.

Risk: Remote API use may incur charges, and retrying ambiguous paid requests can duplicate cost.

Mitigation: Confirm cost-sensitive operations before long text, batches, documents, multiple images, long audio, or agent-initiated calls; avoid automatic retries after ambiguous POST failures.

Risk: The required API key could be exposed if pasted into chat or printed in logs.

Mitigation: Keep MONGOL_AI_SKILL_API_KEY in the local environment or a secret manager, never request the key in chat, and rotate any key that was pasted into a conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youteacher/skills/mongolian-ai-codex)
- [Mongol AI service homepage](https://mongol.open-idea.net)
- [Mongol AI pricing](https://mongol.open-idea.net/#pricing)
- [HTTP request and response contracts](references/HTTP-REQUESTS.md)
- [Routing rules](references/INTERFACE-ROUTING.md)
- [Behavior, privacy, cost, and retries](references/BEHAVIOR-RULES.md)
- [Translation and segmentation](references/TRANSLATION.md)
- [Chat and composition](references/CHAT-COMPLETIONS.md)
- [OCR](references/OCR.md)
- [ASR](references/ASR.md)
- [TTS](references/TTS.md)
- [Word and PDF translation](references/DOCUMENT-TRANSLATION.md)
- [API key handling](references/API-KEY.md)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Plain text business results, saved file paths, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs expose only documented business results such as translated text, OCR text, transcripts, chat responses, saved TTS audio paths, and billing lines when available.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
