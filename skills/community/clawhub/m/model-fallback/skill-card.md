## Description:

Multi-model automatic fallback system that monitors model availability and response conditions, then falls back to configured backup models when the primary model is unavailable, slow, or rate-limited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azure5100](https://clawhub.ai/user/azure5100)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure AI agents with fallback chains across MiniMax, Kimi, Zhipu, and OpenAI-compatible model APIs for availability, latency, rate-limit, and cost-management scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback can route failed requests, including sensitive prompts or regulated data, to configured backup model providers.

Mitigation: Disable fallback or restrict the fallback chain to approved providers for sensitive prompts, regulated workloads, or workloads that must remain with a single provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azure5100/skills/model-fallback)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fallback-chain configuration, health-check guidance, logging guidance, and manual control commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
