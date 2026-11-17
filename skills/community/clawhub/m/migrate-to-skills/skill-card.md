## Description:

Converts eligible Codex rules and slash commands into Agent Skill `SKILL.md` files for `.cursor/skills/`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate project and user Cursor/Codex rules or slash commands into Agent Skills while preserving original body content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bulk-change persistent agent instructions and delete original rule or command files.

Mitigation: Review candidate files before migration and make a backup or require explicit confirmation before deleting originals, especially user-level files.

Risk: Migrated content may preserve unwanted or misleading instructions exactly as written.

Mitigation: Audit migrated skill bodies before enabling or deploying the generated skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/migrate-to-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown skill files, configuration frontmatter, and a concise migration summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create `.cursor/skills/.../SKILL.md` files and remove original `.cursor/rules/*.mdc` or `.cursor/commands/*.md` files after migration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
