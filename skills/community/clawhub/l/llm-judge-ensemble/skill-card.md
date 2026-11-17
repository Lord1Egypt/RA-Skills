## Description:

Build a cost-efficient LLM evaluation ensemble with sampling, tiebreakers, and deterministic validators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to design reproducible LLM-as-judge workflows for comparing generative AI outputs at scale, including model shadow tests and promotion gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sampled evaluation data may be sent to external LLM providers using the user's API keys.

Mitigation: Use only with providers and datasets approved for the deployment context, and review provider data policies before evaluating sensitive data.

Risk: Provider API usage can create cost exposure on high-volume evaluation runs.

Mitigation: Estimate judge sampling costs before large runs and monitor API usage under the user's provider accounts.

Risk: Sampled LLM judging may miss quality issues when used as a promotion gate.

Mitigation: Use full judge coverage for final promotion batches, as described by the artifact guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/llm-judge-ensemble)
- [Project homepage declared in artifact](https://github.com/reddinft/skill-llm-as-judge)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evaluation rubric structure, scoring guidance, cost notes, and operational caveats.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
