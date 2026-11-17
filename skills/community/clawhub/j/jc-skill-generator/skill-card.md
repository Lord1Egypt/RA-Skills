## Description:

Extract completed work into reusable AgentSkills and ask after complex task completion whether to generate a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to recognize completed, reusable workflows and turn them into AgentSkill files after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills can influence future agent behavior if the captured workflow is incorrect or too broad.

Mitigation: Review any generated skill before use and keep instructions scoped to the confirmed workflow.

Risk: End-of-task prompts may appear when reusable work is detected.

Mitigation: Treat prompts as optional and require user confirmation before creating skill files.

## Reference(s):

- [Skill Template](references/skill-template.md)
- [ClawHub Skill Page](https://clawhub.ai/jeremycooper2077/skills/jc-skill-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and SKILL.md file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates skill files only after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
