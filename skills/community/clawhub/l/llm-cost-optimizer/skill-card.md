## Description:

Analyze LLM API usage logs and suggest cost optimizations. Use when you need to reduce LLM spending, compare model costs, find downgrade opportunities, detect caching wins, or compress verbose outputs. Supports OpenAI, Anthropic, Google, DeepSeek, and Meta models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze LLM usage logs, estimate spend by model and task, and identify practical cost optimizations such as model downgrades, prompt caching, and shorter outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM usage logs may contain sensitive operational or customer data.

Mitigation: Analyze only logs you are authorized to use, remove unnecessary sensitive fields before sharing results, and keep input files in a controlled local workspace.

Risk: The embedded pricing table may become stale and could lead to inaccurate savings estimates.

Mitigation: Review model prices against current provider pricing before relying on recommendations for budgeting or procurement decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/llm-cost-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local usage-log input and an embedded pricing table that may require periodic review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
