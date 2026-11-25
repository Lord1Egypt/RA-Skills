## Description:

Diagnoses local Ollama calls and suggests fixes for slow, rejected, truncated, or inefficient requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lognebudo](https://clawhub.ai/user/lognebudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers running local Ollama models use this skill to diagnose latency, context limits, prompt cache reuse, CPU offload, and model fit, then choose a relevant fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned npx llmxray command may run a different package release later.

Mitigation: Pin llmxray to a reviewed version before running it, and review the unresolved reference noted by the incomplete scan.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lognebudo/skills/llmxray-diagnose-ollama-calls)
- [LLMxRay project homepage](https://github.com/LogneBudo/llmxray)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Natural-language diagnostic findings and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local, read-only guidance; the skill does not change settings, models, or files.]

## Skill Version(s):

0.8.12 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
