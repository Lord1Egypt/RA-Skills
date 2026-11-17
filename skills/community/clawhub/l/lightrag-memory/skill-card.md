## Description:

LightRAG Memory provides semantic long-term memory for AI agents using vector embeddings and knowledge graphs, with commands to index, insert, and query memory content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogi98rus](https://clawhub.ai/user/ogi98rus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to maintain searchable long-term memory, retrieve targeted context from memory files, and add new knowledge without rereading entire documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory files and inserted documents may be processed by the configured OpenAI-compatible API.

Mitigation: Use a trusted endpoint, avoid storing secrets in memory files, and use a limited API key.

Risk: Dependency versions are not pinned in requirements.txt.

Mitigation: Pin and review dependency versions before deployment.

Risk: The documented reset command deletes the selected storage directory contents.

Mitigation: Verify LIGHTARG_WORKING_DIR or the storage path before running any reset command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ogi98rus/skills/lightrag-memory)
- [Publisher profile](https://clawhub.ai/user/ogi98rus)
- [Default OpenAI API endpoint](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and plain-text query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY; OPENAI_BASE_URL can point to a trusted OpenAI-compatible endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
