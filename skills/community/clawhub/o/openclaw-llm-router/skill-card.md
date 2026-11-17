## Description:

Intelligent model router for OpenClaw that reads local configuration, classifies available models into Premium, Balanced, and Economy tiers, and routes tasks to a recommended model in the active tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrestinfo](https://clawhub.ai/user/forrestinfo)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect configured model providers and route coding, writing, reasoning, long-context, and automation requests to a suitable model tier. It also provides configuration diagnostics and tier comparison guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw configuration and checks whether common provider API keys are configured.

Mitigation: Use it only in environments where local configuration inspection is acceptable, and review generated diagnostics before sharing them outside the environment.

Risk: The bundled diagnostic script probes local Ollama at localhost:11434 to discover local model availability.

Mitigation: Run the diagnostic only when local Ollama discovery is expected, and treat local model inventory as environment-sensitive information.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/forrestinfo/skills/openclaw-llm-router)
- [ClawHub metadata homepage](https://clawhub.ai/skills/openclaw-llm-router)
- [Model Tiers Reference](references/model-tiers.md)
- [OpenClaw Config Format](references/openclaw-config-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text routing recommendations with inline shell commands and configuration diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report the active tier, recommended model, provider, task type, rationale, cost reference, alternatives, configured provider summary, and setup guidance.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter and README say 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
