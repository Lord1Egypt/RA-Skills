## Description:

Create, edit, improve, audit, validate, and package AgentSkills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystal-k](https://clawhub.ai/user/crystal-k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design new AgentSkills, improve existing SKILL.md files, restructure skill resources, run lightweight validation, and package skills for distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or modified skills can contain incorrect, stale, or misleading instructions.

Mitigation: Review diffs to SKILL.md and bundled resources before packaging or installing generated skills.

Risk: Packaging the wrong directory can include unrelated private files in a .skill archive.

Mitigation: Point packaging only at the intended skill directory and inspect the package contents before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crystal-k/skills/my-skill-name)
- [Publisher profile](https://clawhub.ai/user/crystal-k)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill directories and package .skill archives when the user requests implementation.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
