## Description:

Provides real-time chat, intent recognition, task delegation to sub-agents, and proactive companionship through direct dialogue and agent coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaiqwq](https://clawhub.ai/user/libaiqwq)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a Chinese-language conversational controller that chats directly, detects task intent, and routes task requests toward specialized sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses proactive triggers and may initiate conversation without a direct user request.

Mitigation: Require clear user permission before enabling proactive activation and make trigger timing visible to the user.

Risk: The skill may save chat text locally, and retention controls are not clearly documented.

Mitigation: Avoid sharing secrets or sensitive personal information until memory controls, retention, and deletion behavior are reviewed.

Risk: Server security review classified the release as suspicious because quality and privacy expectations require additional review.

Mitigation: Review the skill before installation and confirm user consent, storage behavior, and activation boundaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libaiqwq/skills/mio-main)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured JavaScript objects with chat, task, or initiation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save chat text locally when memory behavior is active; proactive messages depend on configured hours and probability.]

## Skill Version(s):

1.0.0 (source: server release evidence and config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
