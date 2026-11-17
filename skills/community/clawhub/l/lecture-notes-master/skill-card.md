## Description:

Obsidian lecture notes with recursive atomic decomposition. Generates main note (hub), atomic notes (3+ layers deep, rich structure each), and unlimited glossary entries. Inputs: lectures, articles, videos, URLs, transcripts, PDFs. Outputs: Obsidian markdown with Mermaid diagrams, comparison tables, bilingual terms, wikilinks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schaeferanjon](https://clawhub.ai/user/schaeferanjon)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, researchers, and knowledge workers use this skill to turn lectures, articles, videos, transcripts, PDFs, and other study materials into structured Obsidian notes with bilingual glossary entries, diagrams, review questions, and wikilinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite many local files in an Obsidian vault or caller-supplied output directory.

Mitigation: Confirm the target folder and complete file tree before running, keep backups, and prefer a dedicated sandbox or staging folder.

Risk: Untrusted titles or concept names may influence generated paths and filenames.

Mitigation: Review and sanitize topic, title, concept, and glossary names before file generation.

Risk: URL and video extraction may send provided links or content to external processing tools.

Mitigation: Use URL or video extraction only for content that may be shared with the configured extraction service.

Risk: Optional Python dependencies may affect the local environment.

Mitigation: Install optional dependencies in an isolated, pinned Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/schaeferanjon/skills/lecture-notes-master)
- [Skill instructions](artifact/SKILL.md)
- [Usage examples](artifact/EXAMPLES.md)
- [Configuration](artifact/config.json)
- [Note templates](artifact/templates/)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files for Obsidian, Mermaid diagrams, CSV-backed guidance, and optional PNG visualizations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create multiple local files in a configured or user-supplied Obsidian vault path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
