## Description:

The HeyGen skill helps an agent script and prepare consented AI avatar or talking-head videos, including avatar selection, voice and language planning, B-roll direction, disclosure planning, and human-review handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, creators, and social-media teams use this skill to produce scaled, scripted, multilingual avatar videos for explainers, training, localization, faceless channels, and personalized outreach. It is intended for consented likenesses, AI-disclosed content, and a workflow where HeyGen renders and a human reviews before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A request could use a non-consenting person's likeness or imply an endorsement without permission.

Mitigation: Require consent for any real likeness, refuse impersonation, and use a stock avatar, licensed talent, or a consented digital twin instead.

Risk: Avatar content could mislead viewers if AI involvement is hidden.

Mitigation: Plan clear AI disclosure in the caption and/or on screen, and do not remove disclosure to make content appear real.

Risk: Rendered videos could contain incorrect, off-brand, or noncompliant material.

Mitigation: Keep human review and editing before rendering is accepted or publishing is scheduled.

Risk: HeyGen API keys or billing credentials could be exposed during setup.

Mitigation: Protect API keys, use secure credential storage, and avoid placing secrets in scripts, prompts, or published materials.

## Reference(s):

- [The TALK framework](references/the-talk-framework.md)
- [Consent, disclosure + tools layer](references/consent-disclosure-and-tools.md)
- [HeyGen 2026 capabilities](references/heygen-2026-capabilities.md)
- [Scripts, setup + two worked examples](references/script-and-setup-recipes.md)
- [HeyGen video API endpoint](https://api.heygen.com/v3/videos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with scripts, setup briefs, checklists, and inline commands or configuration when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include avatar/engine choices, voice and language plans, B-roll notes, consent and disclosure checks, and human-review routing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
