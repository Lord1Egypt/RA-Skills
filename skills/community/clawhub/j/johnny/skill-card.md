## Description:

Activates Johnny, a persistent virtual design partner persona for design dialogs that challenges assumptions, keeps discussion focused on the core problem, and answers UX practice questions from expertise, notes, or web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiodor-po](https://clawhub.ai/user/fiodor-po)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, product builders, and design teams use this skill to turn an agent thread into a focused design critique and advisory dialog. It is intended for conversational design reasoning, UX practice guidance, and optional note capture after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes the whole thread's interaction style until the user exits the persona mode.

Mitigation: Use Johnny only for design-dialog threads and explicitly exit the mode when returning to general agent behavior.

Risk: The skill can offer to save decisions, shaped thoughts, open questions, or findings after a topic wraps up.

Mitigation: Review the proposed note content and destination before approving any save action.

## Reference(s):

- [Claude Code Skills documentation](https://code.claude.com/docs/en/skills)
- [ClawHub skill page](https://clawhub.ai/fiodor-po/skills/johnny)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text with optional Markdown notes when explicitly approved]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent thread-level persona mode until the user exits or the thread ends]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
