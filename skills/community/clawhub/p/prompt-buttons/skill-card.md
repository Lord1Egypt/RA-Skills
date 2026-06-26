## Description: <br>
A comprehensive helper skill that wraps agent prompts with short, consistent tappable button menus (Yes/No, single digits, or small option sets) so users can interact via Telegram inline buttons or fall back gracefully to numbered lists on channels without button support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to present concise choice prompts as Telegram inline buttons, with numbered-list fallbacks for channels that do not support buttons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Callback payloads could expose sensitive data if a caller places secrets or raw tokens in callback_data. <br>
Mitigation: Use short opaque identifiers that resolve to server-side state, and never include secrets in callback_data. <br>
Risk: Button presses can trigger high-impact or long-running actions if a calling skill maps callbacks directly to execution. <br>
Mitigation: Require clear confirmation before high-impact actions and acknowledge button callbacks before dispatching long-running work. <br>


## Reference(s): <br>
- [Prompt Buttons on ClawHub](https://clawhub.ai/tanjinlimkelvin-dot/prompt-buttons) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JavaScript helper output and Markdown-style prompt text with button payload metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact Telegram-style button payloads and fallback numbered prompt text; callback data should stay short and should not contain secrets.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
