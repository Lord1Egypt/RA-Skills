## Description:

Bidirectional sync between Obsidian PKM notes and a structured ontology graph, with entity and relationship extraction, graph maintenance, and feedback to improve note structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parthpandya1729](https://clawhub.ai/user/parthpandya1729)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and teams use this skill to turn Obsidian Markdown vault content into a searchable ontology graph for contact, project, client, and team-status analysis. It also generates feedback reports that identify missing information, relationship insights, and template improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Obsidian notes may be copied into persistent searchable ontology and feedback files.

Mitigation: Use a narrow sync configuration, run dry-run first, and protect the output directory with restrictive permissions.

Risk: Contact, team-status, and behavioral-pattern data may be unsuitable to sync without authorization.

Mitigation: Avoid syncing sensitive or employee-monitoring notes unless the organization has approved that use.

Risk: Generated graph.jsonl and feedback reports may retain sensitive information longer than intended.

Mitigation: Review, purge, or rotate generated ontology and feedback files regularly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parthpandya1729/skills/obsidian-ontology-sync)
- [Publisher Profile](https://clawhub.ai/user/parthpandya1729)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, JSONL ontology records, and generated Markdown feedback reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated graph data is stored as persistent JSONL, and feedback is written as Markdown reports.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
