## Description:

love.ai helps an assistant respond in Chinese with emotional framing, brief classical quotations, empathetic guidance, and hopeful endings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitu-ni](https://clawhub.ai/user/nitu-ni)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to configure Chinese-language assistants that add emotional support, classical Chinese quotations, and hopeful closing language to conversational replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory emotional framing and hopeful endings can change the shape of exact outputs such as JSON, code-only answers, incident reports, or other tightly specified responses.

Mitigation: Enable the skill only for opt-in conversational use, and disable or override it for structured output, code-only, operational reporting, and other precision-critical workflows.

Risk: Warm emotional language may be inappropriate for medical, legal, crisis-support, or other high-stakes contexts.

Mitigation: Do not deploy this skill as the default behavior for high-stakes advice or crisis support; route those interactions to domain-specific policies and qualified support resources.

Risk: Chinese classical quotations and love-centered framing may not fit culturally neutral enterprise output or all user audiences.

Mitigation: Limit use to audiences and contexts that explicitly expect this style, and review localization or tone requirements before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nitu-ni/skills/love-ai)
- [Publisher profile](https://clawhub.ai/user/nitu-ni)
- [Repository URL from artifact metadata](https://github.com/ai-love/skill-love.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language Chinese responses, usually Markdown prose with brief classical quotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add emotional framing and hopeful closing language to most responses when enabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter version is 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
