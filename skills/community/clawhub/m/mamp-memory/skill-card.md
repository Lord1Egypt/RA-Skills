## Description:

Mark AI Memory Protocol — persistent, searchable session memory for AI agents. SQLite-only, zero external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rokkiezeng](https://clawhub.ai/user/rokkiezeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use MAMP to give local AI agents persistent, searchable conversation memory across sessions without external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recording can capture more conversation content than intended.

Mitigation: Use manual recording unless broad passive capture is acceptable, and avoid auto_record when conversations may contain sensitive data.

Risk: Conversation history is stored as plaintext SQLite data, including WAL/SHM sidecar files when present.

Mitigation: Use an explicit per-agent database path in a protected directory and treat the database plus sidecar files as sensitive records.

Risk: ClawHub security evidence flags storage behavior that does not match the documentation.

Mitigation: Review the installed version's storage paths before deployment and delete any database or sidecar files that should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rokkiezeng/skills/mamp-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local SQLite memory operations; generated code and commands should be reviewed before execution.]

## Skill Version(s):

1.2.1 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
