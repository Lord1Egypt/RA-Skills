## Description:

Synchronizes Obsidian markdown notes with a structured ontology graph by extracting entities and relationships, running analysis, and generating feedback to improve note structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shi8103312](https://clawhub.ai/user/shi8103312)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and teams use this skill to turn Obsidian notes into a queryable ontology for contact, project, team, and business analysis while keeping notes as the primary source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can centralize sensitive Obsidian note content into plaintext ontology and feedback files.

Mitigation: Use a narrow vault path, run dry-run first, restrict permissions on ontology and feedback directories, and avoid syncing those outputs to shared storage unless reviewed.

Risk: Scheduled cron execution may repeatedly process more note data than intended.

Mitigation: Review extraction outputs before enabling cron, limit configured source paths, and use the least frequent schedule that meets the workflow need.

Risk: Contact and team extraction can collect personal or confidential fields such as email, phone, project assignments, and behavioral patterns.

Mitigation: Disable or remove sensitive extractors when generated graph data may be backed up, synced, or readable by other local users or tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shi8103312/skills/obsidian-ontology-sync-1-0-1)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, Python code references, JSON/JSONL ontology records, and generated Markdown feedback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local plaintext ontology JSONL and feedback Markdown when executed.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
