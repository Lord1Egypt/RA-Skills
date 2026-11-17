## Description:

Helps users interactively create, update, and manage LegionClaw skill packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or revise LegionClaw skills, plan bundled resources, write SKILL.md content, and validate the resulting package before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent changes to skill files in the workspace.

Mitigation: Install it only when file creation and modification are intended, keep host permissions scoped to the skills workspace, and review generated files before use.

Risk: Generated or revised skills may contain incorrect guidance or validation gaps.

Mitigation: Run the bundled validation script and review the generated skill before relying on it in agent workflows.

## Reference(s):

- [SKILL.md specification](references/skill-md-spec.md)
- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/legionclaw-skill-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, file changes, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify LegionClaw skill files and run bundled validation scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
