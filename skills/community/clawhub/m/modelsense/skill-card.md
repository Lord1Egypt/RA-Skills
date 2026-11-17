## Description:

ModelSense recommends the best LLM model and effort level for a user task based on task analysis, benchmark data, and the user's configured providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinbenlv](https://clawhub.ai/user/xinbenlv)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Modelsense when they need help choosing an LLM model, effort level, or provider-backed setup for tasks such as coding, research, writing, math, summarization, and long-context analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included agent instruction can invoke Modelsense early in a session and may switch models after notice rather than explicit consent.

Mitigation: Require explicit confirmation before any model switch or delegation, or remove or override AGENTS.md when installing.

Risk: The update workflow fetches model data from an external API and can commit changed model catalog data.

Mitigation: Audit the GitHub Actions workflow and review model catalog changes before maintaining or publishing updates.

## Reference(s):

- [Modelsense README](artifact/README.md)
- [Benchmark Knowledge Base](artifact/data/benchmarks.yaml)
- [Model Catalog](artifact/data/models.yaml)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [ClawHub Skill Page](https://clawhub.ai/xinbenlv/skills/modelsense)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown recommendation with model, effort level, rationale, cost estimate, alternatives, and optional shell or session commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend a session model switch or sub-agent delegation when requested by the user.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
