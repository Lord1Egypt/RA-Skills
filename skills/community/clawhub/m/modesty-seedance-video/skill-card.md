## Description:

Generate AI videos from text prompts or images with Seedance 2.0 on SkillBoss. Best for short ads, product demos, launch clips, and social videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short Seedance 2.0 videos through SkillBoss from text prompts, first-frame images, or reference images for ads, product demos, launch clips, and social videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to SkillBoss for video generation.

Mitigation: Avoid submitting secrets, private media, or sensitive personal data unless the user's SkillBoss account and data-handling expectations cover that use.

Risk: Video generation uses a pay-as-you-go API key and can incur usage costs.

Mitigation: Confirm requested duration, aspect ratio, and reference images before running generation, and use the smallest useful retry change after API errors.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-seedance-video)
- [SkillBoss Seedance Video](https://skillboss.co/skills/seedance-video)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated video URLs or task payloads, summarizes prompt, duration, and aspect ratio, and reports API errors with retry guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
