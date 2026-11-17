## Description:

Provides on-demand long-term memory storage, retrieval, update, and deletion through a Milvus vector database, with flexible fields for roles, events, projects, tasks, and related memory categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoanco](https://clawhub.ai/user/zuoanco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user explicitly asks to save, query, update, or delete long-term task, project, event, decision, note, or knowledge memories. It is intended for workflows that need structured recall through a configured Milvus service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories may contain sensitive or confidential information in the configured Milvus service.

Mitigation: Avoid saving secrets or confidential data, use a dedicated low-privilege Milvus account, and review memory records before storage.

Risk: Weak transport configuration can expose memory data or credentials.

Mitigation: Prefer TLS/HTTPS Milvus endpoints and keep MILVUS_TOKEN out of shared files and logs.

Risk: Delete, update, and recreate operations can remove or corrupt stored memories.

Mitigation: Review the target collection and memory identifiers before destructive operations, and back up important data before using delete, update, or --recreate.

Risk: Unsafe query construction may expose or modify unintended memory records.

Mitigation: Treat filters and memory identifiers as untrusted input until escaping and confirmation safeguards are fixed.

## Reference(s):

- [Memory Format](references/memory-format.md)
- [ClawHub Skill Page](https://clawhub.ai/zuoanco/skills/long-term-task-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MILVUS_URI and MILVUS_TOKEN configuration before database operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
