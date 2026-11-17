## Description:

My Research Lab 我的研究院 is a personal research-lab agent that helps users collect daily findings, run deeper topic discussions, and turn research ideas into tracked project work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iriswong31](https://clawhub.ai/user/iriswong31)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to operate a personal research workflow: configure a research direction, collect and summarize discoveries, archive outputs, receive pushed briefings, and track follow-up projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses persistent automation, memory, local scanning, storage, and outbound delivery, which can expose sensitive research context or send unwanted briefings if under-scoped.

Mitigation: Before enabling it, explicitly choose the research scope, push destinations, archive location, schedule, and whether memory-derived personalization is allowed.

Risk: SMTP passwords or webhook secrets could be exposed if stored in lab configuration, memory, reports, or archives.

Mitigation: Use a protected secret mechanism and do not write SMTP_PASS or webhook secrets into lab-config.json, memory, generated reports, or archives.

Risk: Recommended browser-control or source skills can expand the skill's access and behavior.

Mitigation: Use pinned installer versions and review any recommended browser-control or source skills before adding them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iriswong31/skills/my-research-lab)
- [Cold start workflow](artifact/references/cold-start.md)
- [Three-layer operation rules](artifact/references/three-layers.md)
- [Self-evolving engine rules](artifact/references/self-evolving.md)
- [Configuration schema](artifact/references/config-schema.md)
- [Channels and tools guide](artifact/references/channels-and-tools.md)
- [Source skills registry](artifact/references/source-skills-registry.md)
- [Cron prompt templates](artifact/references/cron-prompts.md)
- [nuwa-skill](https://github.com/nuwa-skill)
- [aihot-skill](https://aihot.virxact.com/aihot-skill/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, HTML briefings, configuration guidance, and project-tracking text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate daily briefings, archived research notes, topic discussion summaries, and project task lists.]

## Skill Version(s):

3.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
