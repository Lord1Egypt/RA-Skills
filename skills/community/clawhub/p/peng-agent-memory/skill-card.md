## Description:

Provides persistent memory for AI agents to remember facts, learn from experience, and track entities across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penglovemeng](https://clawhub.ai/user/penglovemeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give LLM-powered agents persistent local memory for facts, lessons, and entity context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores cross-session memory in a local SQLite database as persistent plaintext.

Mitigation: Avoid storing secrets, credentials, regulated personal data, or third-party personal details unless there is a clear purpose and consent; restrict access to the database file.

Risk: Deletion and cleanup may not fully remove fact text from the SQLite full-text search index until the reported deletion issue is fixed.

Mitigation: Do not rely on forget() or cleanup as complete erasure; review, back up, or securely remove the database when stronger deletion guarantees are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/penglovemeng/skills/peng-agent-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and local memory data structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite storage by default at ~/.agent-memory/memory.db; memory export is JSON-compatible.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
