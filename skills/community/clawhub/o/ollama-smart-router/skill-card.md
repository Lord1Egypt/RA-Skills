## Description:

Intelligent task routing between local and cloud Ollama LLM instances for cost-efficient responses by routing simple tasks to local models and complex tasks to more capable remote or cloud Ollama instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route prompts across local, remote, or specialist Ollama models based on task complexity, endpoint health, and system capability. It is useful when balancing latency, capability, and infrastructure cost for Ollama-backed agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to remote Ollama endpoints or enriched through search when those features are enabled.

Mitigation: Use only Ollama endpoints you control, prefer local-only or HTTPS-protected remote endpoints, and disable or explicitly configure search before handling sensitive prompts.

Risk: Prompt excerpts, classifications, health data, and conversation turns may be stored locally in logs or SQLite databases.

Mitigation: Avoid entering secrets, set retention expectations for local cache and conversation databases, and clear logs or databases when the stored prompt history is no longer needed.

Risk: The security review marks the release suspicious because user prompts can be sent, stored, and enriched in under-disclosed ways.

Mitigation: Review configuration and runtime behavior before deployment, especially endpoint URLs, search settings, cache paths, and logging behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simoncatbot/skills/ollama-smart-router)
- [Publisher profile](https://clawhub.ai/user/simoncatbot)
- [Classifier prompt reference](references/classifier-prompt.txt)
- [Router configuration](config/router.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Streaming text or Markdown from the selected Ollama model, optionally including code snippets, shell commands, or configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes by complexity score, specialist triggers, endpoint health, and model availability; optional search enrichment may add web context before the model response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
