## Description:

Create, edit, improve, or audit AgentSkills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super9du](https://clawhub.ai/user/super9du)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create new AgentSkills, improve existing SKILL.md files, organize bundled resources, validate structure, and package skills when publishing or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to create or edit SKILL.md files and bundled resources, which may change agent behavior.

Mitigation: Review diffs before accepting generated skill changes.

Risk: Packaging creates shareable skill artifacts and may include unintended files if the target path is wrong.

Mitigation: Use explicit target paths and package only when publishing or sharing is intended.

Risk: Skill guidance may be incorrect or incomplete for a specific organization's agent policy.

Mitigation: Validate the finished skill against the applicable AgentSkills specification and local review requirements before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super9du/skills/openclaw-skills-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill files and package artifacts when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
