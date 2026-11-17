## Description:

The design language that makes AI better at frontend design, with domain-specific references, steering commands, and curated anti-patterns for building or reviewing UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maryambahri](https://clawhub.ai/user/maryambahri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to guide AI agents toward distinctive, production-grade frontend interfaces, including stronger typography, color, layout, motion, interaction, responsive design, and UX writing choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence most UI-related work, which may steer an agent away from established product requirements or design systems.

Mitigation: Review generated UI against the product brief, accessibility requirements, and any existing design system before shipping.

Risk: The skill may ask the agent to read a project-local .impeccable.md file or invoke a context setup command when design context is missing.

Mitigation: Inspect project-local design context and setup commands before relying on them in sensitive repositories.

Risk: The UX-writing guidance is primarily English-language guidance and may not fit localized products.

Mitigation: Adapt labels, errors, and interaction copy to the target locale and review translations with native speakers or localization tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maryambahri/skills/impeccable-uxui)
- [Impeccable homepage](https://github.com/pbakaus/impeccable)
- [Impeccable website](https://impeccable.style)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Polypane](https://polypane.app/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with implementation recommendations and occasional inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide broad UI-related agent behavior and request project-specific design context before work begins.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
