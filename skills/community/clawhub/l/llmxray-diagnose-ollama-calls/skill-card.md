## Description:

Diagnoses local Ollama call performance, prompt fit, cache reuse, and model memory usage with LLMxRay's read-only tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lognebudo](https://clawhub.ai/user/lognebudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify why their local Ollama calls are slow, truncated, or missing prompt-cache reuse, then choose appropriate context and model settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the npm package locally routes Ollama requests through a localhost proxy that may record sensitive prompts.

Mitigation: Install only in trusted environments, pin the package version where reproducibility is needed, and avoid routing highly sensitive prompts unless local recording is acceptable.

## Reference(s):

- [LLMxRay project](https://github.com/LogneBudo/llmxray)
- [Diagnose Ollama Calls on ClawHub](https://clawhub.ai/lognebudo/skills/llmxray-diagnose-ollama-calls)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local diagnostics report prioritized findings and suggested fixes; the tools do not change settings.]

## Skill Version(s):

0.8.11 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
