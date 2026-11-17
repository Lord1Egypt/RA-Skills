## Description:

多模型路由器根据任务特征为代理选择合适的 AI 模型，并帮助平衡成本、速度和质量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use this skill to classify user tasks by complexity, domain, urgency, and budget, then choose an appropriate model or fallback strategy. It is intended for model-routing guidance, cost optimization, and quality-aware model selection in mixed AI workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on common Chinese phrases about model choice or cost optimization.

Mitigation: Invoke it explicitly when model-routing advice is desired, or adjust trigger wording if automatic activation is unwanted.

Risk: Model capability, availability, and pricing guidance can become outdated.

Mitigation: Review recommendations against current provider documentation, pricing, and policy before applying them to production routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-model-router)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with routing decisions, comparison tables, and pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model recommendations should be reviewed against current model availability, pricing, and policy before use.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
