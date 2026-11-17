## Description:

Set up local semantic memory search in OpenClaw using Ollama and nomic-embed-text as a free, private, offline-capable replacement for cloud embedding APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw memory search with a locally running Ollama embedding model, including model selection, base URL settings, search tuning, and restart steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding extra memory paths can index private notes or shared Markdown documents.

Mitigation: Only add directories that are intentionally approved for OpenClaw memory search, and review absolute and recursive paths before enabling extraPaths.

Risk: Misconfigured provider or base URL settings can route requests incorrectly or prevent local Ollama search from working.

Mitigation: Use provider "ollama" with baseUrl "http://127.0.0.1:11434" and verify Ollama is running before restarting OpenClaw.

## Reference(s):

- [Configuration Reference](references/config-reference.md)
- [Troubleshooting](references/troubleshooting.md)
- [Ollama](https://ollama.ai)
- [ClawHub Skill Page](https://clawhub.ai/djc00p/skills/openclaw-ollama-memory)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup and troubleshooting guidance; it does not require cloud embedding API keys.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
