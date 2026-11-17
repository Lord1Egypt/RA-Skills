## Description:

Ask whether the work is a whole admin platform or a single page, then render clickable, in-conversation proposals - shell structure first, palette second - so the user picks without leaving the chat, delegating design direction to an installed design skill when one fits; use when choosing visual direction before implementation, not when the project already has a design system or asked for the finished page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moyanach](https://clawhub.ai/user/moyanach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose a visual direction for an admin console, dashboard, internal tool, or single page before implementation. It presents selectable layout and palette proposals, then hands the selected design tokens to implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell picker’s explanatory copy says confirmation proceeds to interface generation, while the actual follow-up proceeds to palette selection.

Mitigation: Check the selected shell and the next palette step in the follow-up before continuing to implementation.

Risk: Confirming a palette asks the assistant to write project CSS variables and continue generating the interface.

Mitigation: Review the proposed CSS variable changes and interface direction before allowing them to be applied.

Risk: The picker previews may contact Google Fonts.

Mitigation: Use locally hosted fonts or remove the external font imports when previews must not make external requests.

## Reference(s):

- [Oh My UI Style on ClawHub](https://clawhub.ai/moyanach/skills/oh-my-ui-style)
- [Publisher profile: moyanach](https://clawhub.ai/user/moyanach)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, HTML/CSS interface previews, Text prompts]

**Output Format:** [Clickable in-conversation proposals followed by design-token guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive selection for platform shell or page layout and palette; selected tokens are handed off for implementation.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
