## Description:

Helps OpenClaw agents reduce startup context usage by loading skill and memory files only when a task requires them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent maintainers use this skill to configure lazy loading of skills, memory files, and context catalogs so agents load only the material needed for the current task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill may change future agent behavior by encouraging lazy loading through AGENTS.md and SKILLS.md templates.

Mitigation: Review and adapt the templates before merging them into an agent workspace.

Risk: Skill catalogs and memory indexes can expose sensitive project details if populated with private context.

Mitigation: Keep sensitive information out of SKILL.md, SKILLS.md, and memory catalog files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/asif2bd/skills/openclaw-skill-lazy-loader)
- [Project homepage from ClawHub metadata](https://github.com/Asif2BD/openclaw-skill-lazy-loader)
- [Security disclosure](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes templates for SKILLS.md and AGENTS.md plus a local command-line helper that prints skill-loading recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
