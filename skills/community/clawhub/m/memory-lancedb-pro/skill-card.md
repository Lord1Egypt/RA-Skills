## Description:

This skill should be used when working with memory-lancedb-pro, a production-grade long-term memory MCP plugin for OpenClaw AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronx-hu](https://clawhub.ai/user/aaronx-hu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install, configure, verify, and operate memory-lancedb-pro for persistent agent memory. It guides setup for Smart Extraction, hybrid retrieval, memory lifecycle management, multi-scope isolation, local or cloud provider choices, and MCP memory tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to work with API keys and provider credentials.

Mitigation: Use environment variables or a secret manager, and avoid pasting API keys into chat.

Risk: The skill recommends a one-line remote installer and downloaded validator scripts.

Mitigation: Prefer audited local installation paths, or pin and verify the exact remote source before execution.

Risk: Automatic capture, recall, and Smart Extraction can process conversation or memory data through cloud providers.

Mitigation: Use the local Ollama plan or disable autoCapture, autoRecall, and smartExtraction for confidential work; enable cloud providers only after deciding what data may leave the machine.

Risk: Auto-recalled memory content is injected into the agent context and could surface in responses.

Mitigation: Instruct the agent not to quote injected memory context, limit recalled entries, and disable autoRecall for sensitive sessions.

## Reference(s):

- [memory-lancedb-pro ClawHub page](https://clawhub.ai/aaronx-hu/skills/memory-lancedb-pro)
- [Full technical reference](references/full-reference.md)
- [memory-lancedb-pro GitHub repository](https://github.com/CortexReach/memory-lancedb-pro)
- [memory-lancedb-pro setup tools](https://github.com/CortexReach/toolbox/tree/main/memory-lancedb-pro-setup)
- [OpenClaw](https://openclaw.ai)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw configuration snippets, provider setup steps, and MCP memory tool guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact documentation describes the underlying memory-lancedb-pro plugin as v1.1.0-beta.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
