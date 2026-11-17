## Description:

Route tasks to the optimal cloud or local model based on task characteristics — coding, analysis, reasoning, creative, or general.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify prompts and select an appropriate Ollama model for coding, analysis, reasoning, creative, general, or technical work. It supports manual routing, OpenClaw configuration, local-versus-cloud preference, speed preference, and fallback when a preferred model is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic routing may select a cloud-hosted model for prompts that contain private, regulated, credential-bearing, or sensitive content.

Mitigation: Review the registry before enabling auto_route or auto_classify, and prefer local-only settings for sensitive workloads.

Risk: A stale or incorrect model registry can produce poor recommendations or unavailable model selections.

Mitigation: Keep the model registry current and review model strengths, host settings, and fallback ordering before deployment.

Risk: The router checks local Ollama availability and assumes cloud models are available.

Mitigation: Validate cloud model access separately when relying on cloud-hosted entries in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tooled-app/skills/ollama-model-router)
- [Tooled-app publisher profile](https://clawhub.ai/user/tooled-app)
- [Ollama](https://ollama.com)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON configuration, and plain-text routing output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a recommended model ID, reason, task type, and an ollama run command for the supplied task.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
