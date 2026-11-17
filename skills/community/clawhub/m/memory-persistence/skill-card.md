## Description:

Memory Persistence helps AI agents store and retrieve private or shared persistent memories across local, SQLite, GitHub, and Gitee backends, with optional semantic search, summarization, and maintenance tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[529279917](https://clawhub.ai/user/529279917)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to give agents persistent memory storage, retrieval, tagging, semantic search, shared memory exchange, and conversation-to-memory summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories may contain sensitive user or team information.

Mitigation: Install only after review or patching when sensitive data will be stored, and prefer local or SQLite storage unless remote sharing is required.

Risk: Remote GitHub or Gitee backends require repository tokens and can expose memory content if repositories or token scopes are too broad.

Mitigation: Use private repositories, least-privilege tokens, and separate shared-memory repositories only when cross-agent access is intended.

Risk: Imported JSON memory data can write records into the configured storage and should not be treated as trusted by default.

Mitigation: Avoid importing untrusted JSON; review import files before loading them and keep backups before bulk imports or deletes.

Risk: LLM-generated summaries can save inaccurate or overbroad memories.

Mitigation: Review generated memories before saving them, especially when conversation summaries contain preferences, personal facts, or credentials.

Risk: Custom LLM base URLs combined with auto-detected credentials can route prompts or keys to unintended endpoints.

Mitigation: Do not use custom LLM base URLs with auto-detected credentials unless the endpoint and credential handling are explicitly reviewed.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/529279917/skills/memory-persistence)
- [ClawHub publisher profile](https://clawhub.ai/user/529279917)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON memory import and export data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include storage configuration, CLI commands, Python API examples, memory records, summaries, maintenance reports, and import/export JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
