## Description:

Guides agents to identify material knowledge gaps, retrieve only relevant evidence from appropriate sources, and stop when they know enough to make the next decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users apply this skill when missing organizational, historical, or current knowledge could change a decision. It selects accessible sources by role, evaluates retrieved evidence, and explains whether the available knowledge is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may query accessible internal knowledge bases while resolving a material gap.

Mitigation: Before use, confirm retrieval tools and the knowledge-source registry are limited to sources authorized for the task.

## Reference(s):

- [Know Enough on ClawHub](https://clawhub.ai/raguets/skills/know-enough)
- [Overpowered suite (skill metadata)](https://github.com/raguets/overpowered)
- [Adaptive retrieval](references/adaptive-retrieval.md)
- [Knowledge source registry](references/knowledge-source-registry.md)
- [Knowledge sources example](references/knowledge-sources.example.yaml)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise evidence and source references with an ENOUGH / NOT ENOUGH sufficiency judgment.]

## Skill Version(s):

1.0.3 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
