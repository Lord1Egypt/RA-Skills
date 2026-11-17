## Description:

Detect local hardware and recommend local LLM models with fit scoring, quantization guidance, and speed estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexsjones](https://clawhub.ai/user/alexsjones)

### License/Terms of Use:


## Use Case:

Developers and engineers use llmfit to inspect local hardware and choose local LLMs that fit available CPU, RAM, GPU, and VRAM. The skill can guide setup for local inference providers such as Ollama, vLLM, LM Studio, and OpenClaw model defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing a third-party llmfit executable from external distribution channels.

Mitigation: Install only when the publisher and distribution channel are trusted, and verify the installed executable before using the skill for recommendations.

Risk: The skill may guide changes to local OpenClaw model configuration.

Mitigation: Review any proposed openclaw.json diff, confirm the selected model, and keep a backup or revert path for previous defaults.

Risk: Hardware fit and speed estimates can vary by machine and runtime environment.

Mitigation: Validate recommended models on the target hardware before relying on them for production or default local model configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexsjones/skills/llmfit)
- [Publisher profile](https://clawhub.ai/user/alexsjones)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations may include fit levels, quantization choices, speed estimates, and provider-specific model identifiers.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
