## Description:

Install, configure, diagnose, and operate the openclaw-mem0 long-term memory plugin for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyrosveil](https://clawhub.ai/user/nyrosveil)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up OpenClaw agent memory with Mem0, choose platform or self-hosted components, configure persistence, run CLI checks, and troubleshoot memory capture or recall issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic long-term memory can store or recall information that may be inappropriate for a given environment.

Mitigation: Review autoCapture, autoRecall, userId scoping, storage location, deletion through memory_forget, and whether platform or self-hosted mode is appropriate before enabling the plugin.

Risk: Self-hosted mode depends on local Ollama and Qdrant services, so unavailable services can prevent memories from being stored or recalled.

Mitigation: Verify Ollama and Qdrant health before use and follow the troubleshooting checks when memory capture or recall fails.

Risk: Using an implicit latest Qdrant container image can weaken supply-chain control.

Mitigation: Pin the Qdrant image version or digest when stricter deployment control is required.

Risk: A relative history database path can cause a SQLITE_CANTOPEN crash loop when OpenClaw runs as a macOS LaunchAgent.

Mitigation: Set historyDbPath to an absolute writable path, and for older plugin versions set both historyDbPath and historyStore explicitly.

## Reference(s):

- [openclaw-mem0 Troubleshooting](references/troubleshooting.md)
- [Mem0](https://mem0.ai)
- [Mem0 App](https://app.mem0.ai)
- [ClawHub skill page](https://clawhub.ai/nyrosveil/skills/mem0-config)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON5 configuration snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw plugin installation, Mem0 mode selection, local service checks, CLI usage, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
