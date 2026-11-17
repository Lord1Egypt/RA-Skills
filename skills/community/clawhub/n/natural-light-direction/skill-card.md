## Description:

Guides agents to help photographers choose natural light direction, such as front light, 45-degree side light, 90-degree side light, or backlight, based on subject, mood, and shooting context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Photographers and photography-focused agents use this skill to select an outdoor natural-light direction that matches a portrait, landscape, architecture, or texture-focused shooting goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is primarily written for Chinese-language photography guidance while also listing English triggers.

Mitigation: Confirm that the target agent and audience can use Chinese guidance, or add localization review for English-only deployments.

Risk: Photography advice may be unsuitable when the user is asking about artificial lighting, exposure settings, or time-of-day lighting rather than natural light direction.

Mitigation: Route studio lighting, exposure, and golden-hour questions to the neighboring skills identified in the artifact.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/bianchunhui/nyip-photography-skills/tree/main/natural-light-direction)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/natural-light-direction)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown prose with step-by-step recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese or English photography guidance depending on the user's prompt.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
