## Description:

Memory Lucia provides a local SQLite-based memory system for OpenClaw agents with priority analysis, learning tracking, decision records, skill evolution monitoring, local text search, and automatic backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wen521](https://clawhub.ai/user/wen521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent local memory for OpenClaw agents, including priority tracking, learning progress, decision review, skill usage history, and searchable dashboard data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists potentially sensitive agent memory in a local SQLite database and backup files.

Mitigation: Use a dedicated database path, protect database and backup files with local access controls, and avoid storing secrets or regulated data unless retention is approved.

Risk: Backup, rollback, and cleanup behavior can overwrite or delete local memory data.

Mitigation: Review backup, rollback, and cleanup parameters before running them, and keep an external copy of important databases before maintenance operations.

Risk: Security evidence reports unsafe input handling around database queries and cleanup operations.

Mitigation: Prefer a fixed release with input validation and clearer retention controls; otherwise run only in a restricted local workspace after code review.

## Reference(s):

- [Memory V2 API Reference](references/API.md)
- [Artifact README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/wen521/skills/memory-v2-skill)
- [npm Package](https://www.npmjs.com/package/memory-lucia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks; API responses are JSON-like objects backed by local SQLite records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory data and backups on local disk; no external API calls are described in the artifact.]

## Skill Version(s):

2.5.4 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
