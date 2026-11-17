## Description:

Creates AI-generated presentations with 课件帮 (Kejian365), from a user-approved outline and selected theme to a finished online preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[good0007](https://clawhub.ai/user/good0007)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing business reports, product pitches, academic presentations, or training materials use this skill to create and track a presentation, then receive a link to the finished slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a presentation task can deduct from the user's account balance.

Mitigation: Confirm the outline and expected cost before creating a task; avoid duplicate submissions.

Risk: Presentation topics, outlines, requirements, and optional research material are sent to Kejian365.

Mitigation: Avoid including sensitive information unless the user accepts sharing it with the service.

Risk: An account token may be exposed in chat or saved in local task files.

Mitigation: Use a scoped environment secret instead of sharing the token in chat; remove credential-bearing files after use and rotate exposed tokens.

## Reference(s):

- [Kejian365](https://kejian365.com)
- [Kejian365 Open Platform](https://kejian365.com/oapi-portal)
- [Skill API reference](api-reference.md)
- [ClawHub skill listing](https://clawhub.ai/good0007/skills/kejian365-aippt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Presentation links]

**Output Format:** [Markdown with an outline, progress updates, and an online presentation link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slides are generated on Kejian365 and viewed through an online preview link.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
