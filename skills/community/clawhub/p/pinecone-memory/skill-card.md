## Description:

Pinecone Memory uses Pinecone as an OpenClaw semantic memory backend for syncing local memory, semantic querying, index statistics, heartbeat checks, cleanup, backup, and restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenni666](https://clawhub.ai/user/chenni666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect local markdown memory to a Pinecone Integrated Embedding index, then run synchronization, semantic search, health checks, statistics, backup, restore, and namespace cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synchronization can upload local MEMORY.md or memory directory contents to Pinecone more broadly than a user may expect.

Mitigation: Review every sync path, use dry-run first, keep production and test data in separate namespaces, and avoid scheduled sync unless continuous upload is intended.

Risk: Sensitive-data filtering is limited and may not remove all secrets or private notes.

Mitigation: Do not rely on built-in redaction; review or pre-scan memory files, remove sensitive content before sync, and use a least-privilege Pinecone API key.

Risk: Cleanup can remove records from a selected Pinecone namespace.

Mitigation: Confirm the target index and namespace, create a backup first when data should be retained, and require explicit cleanup confirmation.

## Reference(s):

- [Pinecone Memory on ClawHub](https://clawhub.ai/chenni666/skills/pinecone-memory)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)
- [Creating OpenClaw Skills](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, PINECONE_API_KEY, and a Pinecone Integrated Embedding index whose field map uses chunk_text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
