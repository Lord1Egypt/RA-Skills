## Description:

Huo15 Knowledge Base Enterprise helps agents build a Markdown knowledge base, compile raw materials into wiki articles, search and lint the wiki, and synchronize selected articles to Odoo Knowledge with visibility controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise knowledge-base maintainers use this skill to ingest source documents, ask an LLM to compile human-readable Markdown wiki entries, search or health-check the resulting wiki, and export reviewed articles to Odoo Knowledge with workspace, private, or department visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a default Odoo credential in enterprise configuration.

Mitigation: Replace the bundled credential before use, rotate any matching credential in Odoo, and keep secrets out of ordinary knowledge-base articles.

Risk: Odoo export can expose or overwrite knowledge-base articles.

Mitigation: Run exports against a known Odoo target with --dry-run first, review the selected articles, and confirm visibility and department mappings before writing.

Risk: LLM-generated wiki output may contain incorrect filenames, paths, or article content.

Mitigation: Review generated Markdown, source links, and article bodies before indexing, exporting, or using the content as operational knowledge.

Risk: Bulk activation across agents can spread configuration or knowledge-base state more broadly than intended.

Mitigation: Activate only the intended agent environments and review per-agent data directories and configuration before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-knowledge-base-enterprise)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown wiki files, prompt files, index files, health reports, and Odoo Knowledge articles when the corresponding scripts are run.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
