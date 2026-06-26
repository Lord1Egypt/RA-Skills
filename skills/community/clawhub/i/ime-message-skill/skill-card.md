## Description: <br>
Rewrites recognized spoken or informal text into concise, natural chat-ready written messages, and translates only when the user explicitly requests a target language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill after IME or speech-recognition text is already available, to polish short chat messages before sending. It is intended for text cleanup and optional requested translation, not direct audio transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User message text may be sent to an external model provider. <br>
Mitigation: Use the skill only when the configured provider and retention policy are acceptable, and avoid passwords, secrets, sensitive private conversations, and medical, legal, or financial details. <br>
Risk: Automatic rewriting can change tone or meaning before a message is sent. <br>
Mitigation: Review the rewritten message before sending and keep a path to restore the original recognized text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hei-MaoM/ime-message-skill) <br>
- [Model API notes](references/api_cn.md) <br>
- [Product integration notes](references/integration_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text final message, with guidance for integration and configuration when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The default flow returns only the rewritten text and avoids exposing raw API JSON unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
