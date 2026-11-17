## Description:

MemVault provides a Docker-based long-term memory server for AI agents with Ebbinghaus decay, strength-weighted retrieval, memory statistics, and multi-agent memory tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjy9902](https://clawhub.ai/user/wjy9902)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use MemVault to add persistent, queryable memory across agent sessions, including daily decay, access-based memory strengthening, and per-agent memory tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default deployment may expose persistent memory data too broadly.

Mitigation: Bind services to 127.0.0.1 or a private network and add API authentication before use with sensitive memory content.

Risk: The installer can run an external curl-to-shell path for Ollama installation.

Mitigation: Review or remove the automatic Ollama install step and install dependencies through an approved package-management process.

Risk: Default database credentials are included in the deployment configuration.

Mitigation: Replace default PostgreSQL credentials and protect the database before storing production or sensitive memories.

Risk: Memory content may be sent to a configured non-local OpenAI-compatible LLM endpoint.

Mitigation: Explicitly approve the LLM endpoint and data handling policy before enabling non-local providers.

## Reference(s):

- [MemVault ClawHub listing](https://clawhub.ai/wjy9902/skills/memvault)
- [Publisher profile](https://clawhub.ai/user/wjy9902)
- [Docker installation documentation](https://docs.docker.com/get-docker/)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide installation and operation of a local memory server, CLI commands, HTTP API calls, and environment configuration.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
