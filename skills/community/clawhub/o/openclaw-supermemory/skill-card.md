## Description:

Supermemory gives agents long-term memory with atomic fact extraction, relational versioning, semantic search, entity profiles, and local-first storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jared-goering](https://clawhub.ai/user/jared-goering)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Supermemory to add cross-session recall, semantic search, and entity-aware memory to agents while preserving version history of facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and serves sensitive cross-session agent memory.

Mitigation: Treat the memory database as private data and define clear redaction, retention, and deletion controls before auto-ingesting conversations.

Risk: Automatic ingestion and external LLM-based extraction can process sensitive conversation content.

Mitigation: Avoid auto-ingesting sensitive conversations unless inputs are reviewed, redacted, and covered by the configured LLM provider's data handling terms.

Risk: The local API and plugin can expose memory data if installed or served without appropriate controls.

Mitigation: Use a pinned, trusted package version, inspect the plugin source, and keep the API bound to localhost or protected by authentication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jared-goering/skills/openclaw-supermemory)
- [PyPI package](https://pypi.org/project/openclaw-supermemory/)
- [GitHub repository](https://github.com/jared-goering/openclaw-supermemory)
- [OpenClaw plugin](https://github.com/jared-goering/openclaw-supermemory/tree/main/plugin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localhost API usage, CLI commands, and memory-ingestion guidance.]

## Skill Version(s):

0.2.1 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
