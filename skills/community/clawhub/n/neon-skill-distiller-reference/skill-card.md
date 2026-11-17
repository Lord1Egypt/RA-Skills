## Description:

Complete skill compression documentation - all options, modes, and calibration details (~2,500 tokens).

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this reference skill to compress verbose agent skills, choose compression modes, and report functionality trade-offs for reduced context-window usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local calibration history may store details about compression runs in the workspace.

Mitigation: Decide whether local calibration logging is acceptable before using the skill, especially in shared or sensitive workspaces.

Risk: Compressed skills can omit context that a downstream agent may need for edge cases.

Mitigation: Review the reported removals, functionality score, and generated compressed skill before deployment.

Risk: Cloud LLM providers may process the skill content being compressed when provider keys are configured.

Mitigation: Use a local provider for sensitive skill material or confirm the configured provider is approved for the content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/neon-skill-distiller-reference)
- [Project homepage](https://github.com/live-neon/skills/tree/main/skill-distiller/reference)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compressed skill content, token estimates, functionality preservation scores, and calibration notes.]

## Skill Version(s):

0.2.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
