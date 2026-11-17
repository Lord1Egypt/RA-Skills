## Description:

Infinity Context helps agents preserve long-session details by compressing working context, archiving redacted conversation chunks in a local SQLite/FTS5 store, and retrieving exact prior details on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pondsi](https://clawhub.ai/user/pondsi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to keep long agent sessions searchable after context compaction while retaining recent working context for active reasoning. It is suited to local workflows where exact recall matters and users accept a local sensitive-history archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores searchable local conversation history that may contain sensitive information even after redaction.

Mitigation: Use it only when local session retention is desired, keep archives out of synced or shared folders, and treat archive files as sensitive data.

Risk: Local retention can preserve more history than the user intends.

Mitigation: Review retention settings, keep the default bounded retention unless longer storage is required, and use INFINITY_CONTEXT_NO_ARCHIVE=1 or cleanup commands when history should not be retained.

Risk: Maintenance operations can mutate local files or permanently delete expired archive files.

Mitigation: Run destructive cleanup deliberately with the documented confirmation flags and scope in-place redaction to an explicit allowed directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pondsi/skills/infinitycontext)
- [Architecture](references/architecture.md)
- [Other languages](references/languages.md)
- [Release changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite/FTS5 archives and read-only retrieval results when the user runs the bundled scripts.]

## Skill Version(s):

1.8.7 (source: SKILL.md frontmatter, CHANGELOG.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
