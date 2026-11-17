## Description:

Automatically assesses task complexity and adjusts reasoning level before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a preprocessing guide to classify prompt complexity and decide when deeper reasoning should be enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reasoning-mode changes can increase latency or token use when speed matters.

Mitigation: Follow the documented quick-answer, time-sensitive, and auto-downgrade conditions, and use the explicit off control when needed.

Risk: The visual indicator convention may alter response presentation for high-complexity prompts.

Mitigation: Review the icon convention before deployment and disable or adapt it where plain responses are required.

## Reference(s):

- [Adaptive Reasoning on ClawHub](https://clawhub.ai/marjoriebroad/skills/mar-adaptive-reasoning)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append a reasoning-mode indicator to high-complexity responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
