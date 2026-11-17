## Description:

Manage and query a persistent SQLite-based graph of people and their relationships for personal CRM, org charts, mentorship, and collaboration mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makkzone](https://clawhub.ai/user/makkzone)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to store, update, search, and export people relationship graphs for professional network management, organizational mapping, mentorship tracking, and collaboration analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive personal details and relationship notes in a local SQLite database and exported graph JSON.

Mitigation: Protect people.db and exported JSON files, avoid storing unnecessary sensitive details, and apply local access controls appropriate for personal contact data.

Risk: Deletion, cascade deletion, or duplicate-prevention behavior may not fully match release claims in this version.

Mitigation: Keep backups before deletions and verify relationship records after bulk edits or imports.

## Reference(s):

- [People Strategy ClawHub Skill Page](https://clawhub.ai/makkzone/skills/people-strategy)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, and JSON graph output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local SQLite-backed records and exported graph JSON containing sensitive personal or relationship data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
