## Description:

Weave maintains a private, provenance-backed social graph of people, relationships, preferences, and shared experiences for meeting prep, gift ideas, hosting, introductions, city connections, and serendipity discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Weave to store, retrieve, query, import, export, and synchronize private relationship knowledge with provenance-backed records and explicit writeback approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily automatic self-update can silently replace skill files from the configured source.

Mitigation: Remove automatic updates or make them explicit opt-in with signed, pinned releases and visible approval before replacement.

Risk: The skill stores and exports personal relationship and contact data in local database, staging, and journal paths.

Mitigation: Limit filesystem access, protect exported and staged files, and review retention and sharing practices before use.

Risk: Google Contacts and Clay sync can write data back to external systems.

Mitigation: Keep writeback disabled by default and require explicit approval for each sync or writeback action.

## Reference(s):

- [Weave ClawHub Page](https://clawhub.ai/indigokarasu/skills/ocas-weave)
- [README](README.md)
- [Connectors](references/connectors.md)
- [Schemas](references/schemas.md)
- [Query Patterns](references/query_patterns.md)
- [Import & Export](references/import_export.md)
- [Journal](references/journal.md)
- [vCard Projection](references/vcard_projection.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Cypher, JSON, shell command, configuration, journal, and vCard text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local database, staging, configuration, export, and journal files; external writeback requires explicit per-sync approval.]

## Skill Version(s):

2.3.0 (source: server release metadata, README changelog, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
