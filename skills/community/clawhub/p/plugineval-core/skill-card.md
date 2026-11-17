## Description:

Self-contained PluginEval quality evaluation engine that measures 6 dimensions, detects anti-patterns, and assigns badges without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donmeusi](https://clawhub.ai/user/donmeusi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use PluginEval Core to evaluate AI agent skill quality before installation, during improvement, or before publishing to ClawHub with quality badges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional write mode can modify SKILL.md, remove empty reference files, and delete old backups when run against a target skill directory.

Mitigation: Use read-only evaluation modes by default, and only run --auto-fix --allow-write on trusted skill directories that have been checked for symlinks.

## Reference(s):

- [Quality Framework](references/quality-framework.md)
- [Anti-Pattern Catalog](references/anti-pattern-catalog.md)
- [ClawHub Skill Page](https://clawhub.ai/donmeusi/skills/plugineval-core)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text and JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes score, grade, badge, dimension scores, anti-patterns, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
