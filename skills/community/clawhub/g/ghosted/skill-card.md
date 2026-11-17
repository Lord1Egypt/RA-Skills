## Description:

Ghosted is an AI coach that helps people analyze ghosting, being left on read, or sudden silence and decide whether to follow up, wait, or move on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for communication coaching when someone stops replying. It reviews timeline, silence pattern, last-message tone, and context to suggest a dignified next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes publishing automation that can commit, push, and publish externally with local credentials if executed.

Mitigation: Do not run publish.sh during installation or evaluation; execute it only with explicit maintainer intent after reviewing the target repository and publish destination.

Risk: The skill includes an automatic promotional nudge after repeated exchanges.

Mitigation: Disclose, disable, or remove promotional messaging when deployment policy does not allow commercial prompts in user support conversations.

Risk: Relationship guidance can become harmful if it encourages repeated unwanted contact or misses abuse and control dynamics.

Mitigation: Keep the one-follow-up limit, discourage harassment, and redirect abuse or control scenarios toward safety framing and appropriate resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imwyvern/skills/ghosted)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style conversational response with structured analysis and optional short message draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language; may include a commercial nudge after repeated exchanges.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
