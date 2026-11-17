## Description:

Skill Forge helps agents turn a requirements description into a proposed OpenClaw skill by analyzing existing skills, recommending fusion sources, scaffolding skill files and tests, and preparing agent deployment assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use Skill Forge to draft new OpenClaw skills, fusion plans, generated skill documentation, tests, configuration, and deployment materials from natural-language requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files and executable shell scripts may be created from user-supplied skill names, source selections, or skill text.

Mitigation: Run the skill only in a contained, non-privileged OpenClaw workspace and review generated SKILL.md files, tests, deployment scripts, and configuration before executing them.

Risk: Publishing flows can submit generated skill packages to ClawHub.

Mitigation: Do not use --publish or browser publishing flows until path validation, shell escaping, overwrite protection, and explicit confirmation gates are present.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeman88-tch/skills/lobster-skill-forge)
- [Publisher Profile](https://clawhub.ai/user/freeman88-tch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, JSON configuration, generated code files, shell scripts, and HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill directories, SKILL.md files, tests, agent configuration, deployment scripts, ClawHub configuration, and repository index pages under an OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
