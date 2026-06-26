## Description: <br>
Use for Mongolian-language work through the Mongol Open Idea API, including Chinese, traditional Mongolian, and Cyrillic Mongolian translation; Mongolian chat or writing; TTS; ASR; OCR; and Word/PDF document translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youteacherasia](https://clawhub.ai/user/youteacherasia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route Mongolian translation, chat, OCR, ASR, TTS, and document translation tasks through the Mongol Open Idea API with credential and billing safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided Mongol Open Idea API key. <br>
Mitigation: Configure the key as MONGOL_OPEN_IDEA_API_KEY, do not paste it into chat, and revoke any key that was exposed. <br>
Risk: Calls to the external API may incur charges. <br>
Mitigation: Confirm long text, batch, document, OCR, ASR, and TTS work before sending paid requests, and avoid repeating a charged request without explicit approval. <br>
Risk: Billing and account balance fields may expose account metadata. <br>
Mitigation: Parse billing fields for cost awareness, but show them only when the user explicitly asks for cost, charge, billing, or balance details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youteacherasia/mongolian-ai-codex) <br>
- [Publisher profile](https://clawhub.ai/user/youteacherasia) <br>
- [Mongol Open Idea API base](https://mongol.open-idea.net/api/v1) <br>
- [API Reference](references/api-reference.md) <br>
- [Behavior Rules](references/behavior.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands, configuration guidance, and saved audio files for TTS workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final answers should contain business content only unless the user explicitly asks for billing details; TTS audio is saved or played rather than printed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
