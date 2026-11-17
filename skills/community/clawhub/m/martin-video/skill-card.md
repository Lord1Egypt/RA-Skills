## Description:

Generate MP4 videos through SkillBoss API Hub with prompt-based controls for duration, aspect ratio, optional model hints, and optional image input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate short MP4 video clips from text prompts, with optional reference images, using an external SkillBoss/HeyBoss API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference images, and the SkillBoss API key are sent to an external API service.

Mitigation: Avoid regulated or sensitive media unless organizational policy approves the service, and run the skill in a constrained environment.

Risk: The skill depends on ordinary API-key handling and runtime network access.

Mitigation: Store SKILLBOSS_API_KEY outside source files, rotate it if exposed, and review dependency locking before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-video)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples and generated MP4 media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may send prompts and optional reference images to the external SkillBoss/HeyBoss API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
