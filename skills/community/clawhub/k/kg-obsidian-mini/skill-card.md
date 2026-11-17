## Description:

Kg Obsidian Mini helps an agent organize Obsidian knowledge graph notes by classifying note types, planning changes before edits, normalizing links, creating relationship notes, deduplicating related notes, and previewing YAML-based enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and Obsidian vault maintainers use this skill to have an agent inspect notes, produce an execution checklist, and then apply controlled cleanup for note classification, link normalization, relationship notes, deduplication, and enrichment planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad note edits, renames, moves, deletions, and relationship-note creation across an Obsidian vault.

Mitigation: Review the generated dry-run checklist before execution, require explicit approval for destructive operations, and keep backups or version control enabled.

Risk: Web enrichment can expose note-derived search terms to external services.

Mitigation: Use enrichment only when external search is acceptable for the selected notes, and avoid sending sensitive note content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realpda/skills/kg-obsidian-mini)
- [Publisher profile](https://clawhub.ai/user/realpda)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task lists, Obsidian note updates, shell commands, and JSON preview output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only analysis checklists, YAML validation output, and enrichment previews.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
