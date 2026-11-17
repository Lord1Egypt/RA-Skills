## Description:

Complete methodology for local LLM performance optimization using a four-phase control-variable process to tune llama.cpp and llama-server parameters across hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoperealize](https://clawhub.ai/user/hoperealize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark local llama.cpp and llama-server deployments, compare launch parameters, and produce recommended configurations for performance, context length, and stability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example llama-server commands could expose a local model service if copied into an externally reachable deployment.

Mitigation: Keep llama-server bound to localhost unless a reverse proxy, HTTPS, and deployment-specific access controls are configured.

Risk: Parameter tuning can trigger out-of-memory failures or mismatched context settings on local hardware.

Mitigation: Validate settings against the target GPU and align OpenClaw contextWindow and maxTokens with the selected llama-server context size.

Risk: Cloud model checks used during tuning may receive sensitive prompts if operators reuse private test data.

Mitigation: Use non-sensitive prompts for cloud validation and keep private or regulated content out of external model calls.

## Reference(s):

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [ClawHub skill page](https://clawhub.ai/hoperealize/skills/llama-params-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with benchmark tables, command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hardware-specific recommendations that should be validated on the target machine.]

## Skill Version(s):

3.1.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
