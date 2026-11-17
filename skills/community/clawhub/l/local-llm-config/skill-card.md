## Description:

Set up, manage, and optimize locally-hosted LLMs for agents with automated detection, configuration, and benchmarking capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to detect local LLM backends, compare available models, configure a model for agent use, and benchmark its performance. It supports workflows using Ollama, LM Studio, and llama.cpp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced command may not come from the expected source.

Mitigation: Verify the command's source before running it.

Risk: Switching or resetting models may overwrite existing configuration.

Mitigation: Back up the current configuration before switching or resetting models.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Ollama](https://ollama.com)
- [LM Studio](https://lmstudio.ai)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Text reports and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backend detection results, model specifications, benchmark metrics, and generated configuration content.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
