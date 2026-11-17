## Description:

A comprehensive helper skill that wraps agent prompts with short, consistent tappable button menus (Yes/No, single digits, or small option sets) so users can interact via Telegram inline buttons or fall back gracefully to numbered lists on channels without button support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use Prompt Buttons to build concise choice prompts with Telegram inline buttons and numbered-list fallbacks for channels without button support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper sends an additional hard-coded Chinese confirmation message after button delivery, which may be unsuitable for deployments that need strict localization or quiet message behavior.

Mitigation: Review, localize, or disable the confirmation message before deployment in channels where extra messages are not acceptable.

Risk: Callback payloads can carry sensitive state if a caller places raw secrets, tokens, or detailed user data in callback_data.

Mitigation: Use short opaque identifiers that map to server-side state, and keep secrets or sensitive data out of callback_data.

Risk: The skill guidance suggests acknowledging button presses and dispatching long-running work in background subagents, which may be too permissive for environments requiring tight control over background work.

Mitigation: Require explicit handler allowlists and approval gates before any button callback starts long-running or background actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanjinlimkelvin-dot/skills/prompt-buttons)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript helper code and message payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces button metadata for message payloads and fallback numbered-list prompt text.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
