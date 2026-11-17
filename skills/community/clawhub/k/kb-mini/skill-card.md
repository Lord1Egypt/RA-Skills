## Description:

Kb Mini stores, searches, and automatically manages a personal or shared SQLite knowledge base for OpenClaw agents through command-line tools and before/after hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasliu](https://clawhub.ai/user/thomasliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist useful conversation context, retrieve prior notes, and share a lightweight knowledge base across agents. It is suited to workflows that need local recall and capture while accepting the privacy and review obligations of persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save full conversation turns into a persistent local knowledge database.

Mitigation: Enable it only with explicit capture expectations, prefer a private KB path, and provide review and deletion controls for retained entries.

Risk: Stored conversations can retain secrets or sensitive personal and business information.

Mitigation: Avoid sharing secrets while the skill is enabled and require secret redaction before using it for sensitive work.

Risk: The security evidence reports serious injection flaws in database access.

Mitigation: Require parameterized database access and review the storage and retrieval scripts before installation or deployment.

Risk: Automatic summarization and recall can surface stale, excessive, or inappropriate context to an agent.

Mitigation: Use safe summarization limits, prefer scoped recall, and review captured entries before relying on them in high-impact workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thomasliu/skills/kb-mini)
- [API Interface Specification](artifact/references/api-spec.md)
- [Database Schema](artifact/references/db-schema.md)
- [Retrieval Pipeline](artifact/references/retrieval-pipeline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists knowledge-base entries in a local or shared SQLite database and may inject concise recall context before agent work.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact SKILL.md says v1.2.0 and artifact/_meta.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
