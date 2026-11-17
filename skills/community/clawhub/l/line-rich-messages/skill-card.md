## Description:

Guides agents in creating LINE Rich UI responses, including Flex Messages, buttons, quick replies, and markdown auto-conversion for lower-friction mobile conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shingo0620](https://clawhub.ai/user/shingo0620)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to design LINE chat experiences with quick replies, button cards, Flex Message JSON, and markdown-to-card formatting while avoiding unnecessary typed replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inline LINE button capabilities may change how users interact with agent responses.

Mitigation: Enable the OpenClaw LINE plugin and inline button capability only in intended channels and confirm the configuration before deployment.

Risk: Template examples include Traditional Chinese sample text that may be unsuitable for all audiences.

Mitigation: Review and localize visible template labels and message text before using them with end users.

Risk: Stale README references to file delivery could confuse reviewers or operators.

Mitigation: Rely on SKILL.md and the release changelog, which state that file upload and sharing workflows were removed for security.

Risk: LINE Flex Message text is not selectable or copyable in clients.

Mitigation: Send copy-sensitive content such as IDs, keys, and URLs as plain text instead of Flex Messages or markdown that triggers card conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shingo0620/skills/line-rich-messages)
- [Publisher profile](https://clawhub.ai/user/shingo0620)
- [LINE UI Decision Matrix](references/decision-matrix.md)
- [LINE Directives Guide](references/directives.md)
- [LINE Flex Message Templates](references/flex-templates.md)
- [LINE Markdown Auto-Conversion](references/markdown-to-flex.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with LINE directives and Flex Message JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw LINE plugin configuration for inline button behavior.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
