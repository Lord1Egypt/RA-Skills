## Description:

Intelligently recommends optimal AI models based on task requirements by reading the user's OpenCLAW configuration and providing context-aware model suggestions across major global and domestic model providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garygou1024](https://clawhub.ai/user/garygou1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenCLAW users use this skill to choose suitable configured AI models for coding, image analysis, reasoning, long-document, fast-response, and Chinese-language tasks. It adapts recommendations to model IDs available in the user's local OpenCLAW configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to read local OpenCLAW model configuration, and model IDs or provider names may be sensitive in some environments.

Mitigation: Use the skill only where reading configured model IDs is acceptable, and avoid it in contexts where model configuration names are sensitive.

Risk: Keyword-based model matching can produce recommendations that do not fully reflect current model capabilities or policy constraints.

Mitigation: Review the recommended model against the user's task, available configuration, and applicable model-use policies before acting on the recommendation.

## Reference(s):

- [Model Capability Reference](references/comparison.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are scoped to models available in the user's OpenCLAW configuration.]

## Skill Version(s):

1.0.0 (source: skill.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
