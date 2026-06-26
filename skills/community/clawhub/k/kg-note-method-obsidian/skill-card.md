## Description: <br>
Organizes Obsidian vaults with the KG note method, including note typing, link rules, relationship notes, naming checks, deduplication, enrichment, and layered loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpda](https://clawhub.ai/user/realpda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian users and agents use this skill to audit, reorganize, and enrich Markdown notes while preserving original wording where possible. It guides note classification, relationship-note creation, YAML validation, duplicate handling, and task checklist tracking for KG-style vault maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify notes and filenames in an Obsidian vault. <br>
Mitigation: Use kg 检查 for preview-before-edit behavior, keep backups or version control, and review _working task files before resuming old work. <br>
Risk: Web, image lookup, or enrichment steps may expose private note topics or URLs externally. <br>
Mitigation: Avoid lookup and enrichment steps for private notes unless that external disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realpda/kg-note-method-obsidian) <br>
- [YAML Frontmatter Parsing Pitfalls](references/yaml-parsing-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown checklists, Obsidian note edits, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Markdown files under the user's Obsidian vault and _working task directory.] <br>

## Skill Version(s): <br>
3.23.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
