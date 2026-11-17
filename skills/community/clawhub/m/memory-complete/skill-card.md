## Description:

Complete Memory System - Unified integration of all memory features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[717986230](https://clawhub.ai/user/717986230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a persistent local memory system with structured SQLite storage, optional vector retrieval, diary entries, emotional analysis, Theory of Mind reasoning, and configurable retrieval strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores prompts, notes, diary-like entries, inferred beliefs and emotions, and platform-message content in a local SQLite memory database.

Mitigation: Install only when persistent local memory is appropriate; restrict database file access, review stored data, and avoid adding sensitive content that should not be retained.

Risk: Optional Ollama embeddings can send memory content to a configured HTTP endpoint.

Mitigation: Keep Ollama disabled unless the endpoint is trusted, and avoid remote ollama_url values unless sending memory content there is acceptable.

Risk: Installation and verification create and modify a local database.

Mitigation: Run setup in a controlled workspace, review database paths before execution, and back up or isolate existing memory data.

## Reference(s):

- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/717986230/skills/memory-complete)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local database setup, memory queries, retrieval configuration, and optional Ollama embedding configuration.]

## Skill Version(s):

4.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
