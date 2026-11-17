## Description:

Provides structured long-term memory for OpenClaw agents with semantic, keyword, and knowledge graph retrieval, entity extraction, temporal versioning, and experiential learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ascottbell](https://clawhub.ai/user/ascottbell)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to replace the default OpenClaw memory backend with a self-hosted long-term memory service that can store, retrieve, and delete conversation-derived memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs external packages for the maasv server and OpenClaw memory plugin.

Mitigation: Review the maasv and @maasv/openclaw-memory packages before installation and consider pinning exact versions.

Risk: Conversation summaries may be stored in a local SQLite memory database and sent to the selected LLM or embedding provider when cloud providers are configured.

Mitigation: Enable autoCapture only after confirming that local storage and provider data handling are acceptable; use local providers such as Ollama when no external calls are desired.

## Reference(s):

- [maasv Memory ClawHub listing](https://clawhub.ai/ascottbell/skills/maasv-memory)
- [@maasv/openclaw-memory plugin](https://www.npmjs.com/package/@maasv/openclaw-memory)
- [maasv server and core package](https://pypi.org/project/maasv/)
- [maasv README](https://github.com/ascottbell/maasv)
- [Qwen3-Embedding via Ollama](https://ollama.com/library/qwen3-embedding)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for installing a local memory server, configuring OpenClaw, and using memory tools.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
