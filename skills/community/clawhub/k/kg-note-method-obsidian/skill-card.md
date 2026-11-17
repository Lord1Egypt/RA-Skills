## Description:

Organizes Obsidian vault notes with the KG note method by classifying note types, normalizing naming and links, deduplicating relationships, and preparing checklist-driven corrections and enrichments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users and agents use this skill to inspect, reorganize, and enrich Markdown vault notes into KG-style concept, object, skill, and relation notes. It is intended for checklist-driven note maintenance, relationship cleanup, YAML validation, and controlled vault edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly modify, rename, delete, and enrich Obsidian vault notes.

Mitigation: Use the explicit kg 检查 preview flow before applying changes, keep vault backups, and review generated execution checklists before file edits.

Risk: File operations could affect notes outside the intended workspace if the working path is too broad.

Mitigation: Restrict the working path to the intended Obsidian vault and verify checklist files are created under that vault's _working directory.

Risk: Enrichment can append externally sourced or unreviewed content to notes.

Mitigation: Preview enrichment output with --stdout and review external search results before appending them to vault files.

## Reference(s):

- [YAML Frontmatter Parsing Pitfalls](references/yaml-parsing-pitfalls.md)
- [ClawHub skill page](https://clawhub.ai/realpda/skills/kg-note-method-obsidian)
- [Publisher profile](https://clawhub.ai/user/realpda)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and checklists with inline shell commands and Python helper script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, rename, delete, validate, or enrich Obsidian Markdown files in the selected vault.]

## Skill Version(s):

3.23.0 (source: evidence.release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
