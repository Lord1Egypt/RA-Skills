## Description:

Enter GPT strong execution mode for the current conversation when explicitly invoked, such as with /gpt-go. Persist across the conversation. Default to execution, treat short directives as authorization to continue, minimize words, and stop only at explicit high-risk boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-joey](https://clawhub.ai/user/c-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users invoke this skill when they want a conversation-scoped execution posture that moves directly through clear tasks, keeps replies short, and pauses at explicit high-risk boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the assistant to move faster, ask fewer routine questions, and treat brief follow-ups as permission to continue.

Mitigation: Use it only when that execution posture is desired, and require explicit confirmations for sensitive, production, financial, privacy, permission-changing, or destructive work.

Risk: Short continuation directives can reduce opportunities to catch ambiguity during a task.

Mitigation: Turn off or override the skill when step-by-step review is needed, and give an explicit stop or decision request before high-risk work proceeds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-joey/skills/gpt-go)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown and plain text behavioral guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation-scoped behavior guidance; no separate output artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
