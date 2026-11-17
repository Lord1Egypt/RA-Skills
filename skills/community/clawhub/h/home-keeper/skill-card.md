## Description:

Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasgo24601](https://clawhub.ai/user/lucasgo24601)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to design, create, validate, package, and iterate on Codex AgentSkills with appropriate structure, metadata, resources, and supporting scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited SKILL.md files can influence future agent behavior.

Mitigation: Review generated diffs before installing or sharing created skills, and keep trigger descriptions clear and narrowly scoped.

Risk: Bundled helper scripts can create directories, write skill files, and produce .skill archives in caller-specified locations.

Mitigation: Use explicit target directories, inspect package contents before distribution, and rely on the packaged validation and symlink-skipping behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasgo24601/skills/home-keeper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code snippets and shell commands; bundled scripts can create SKILL.md files, resource placeholders, validation output, and .skill archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include filesystem changes in caller-specified skill directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
