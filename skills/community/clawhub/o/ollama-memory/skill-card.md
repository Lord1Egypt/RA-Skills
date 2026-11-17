## Description:

Provides guidance for a local AI assistant memory system using Markdown records, SQLite vector storage, and Ollama embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up and operate a local long-term memory workflow for AI assistants, including daily notes, long-term memory files, local embeddings, and semantic search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reloads user and session memories.

Mitigation: Define consent, retention, and deletion rules before use, then periodically review and delete memory files.

Risk: Stored memories may contain secrets or personal information.

Mitigation: Avoid saving secrets, real account details, or private personal data in memory files.

Risk: Changes to SOUL.md or MEMORY.md can alter long-term assistant behavior.

Mitigation: Require user confirmation before changing personality or long-term behavior files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kk-kingkong/skills/ollama-memory)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance depends on local files, Ollama, SQLite, and Python scripts configured by the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
