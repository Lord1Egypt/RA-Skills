## Description:

Route each user request to the most cost-effective model or multi-model workflow based on task type, complexity, risk, latency, budget, tool needs, and verification requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephensu66](https://clawhub.ai/user/stephensu66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose model tiers, workflow shapes, and verification strategies for production agent requests while balancing cost, speed, quality, exactness, and risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-routing guidance can recommend an unnecessarily expensive or underpowered workflow if request risk, exactness, tool availability, or modality needs are misread.

Mitigation: Review routing recommendations against the skill's hard routing rules, especially for high-risk, exact, long-context, coding, or multimodal tasks.

Risk: The skill influences downstream model-selection decisions but does not itself execute commands or access data.

Mitigation: Treat its output as advisory and review recommendations before applying them in production orchestration or policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stephensu66/skills/model-routing-orchestrator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown routing decision with task profile, execution plan, model role assignment, cost rationale, escalation rule, and fallback rule]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory routing recommendations only; it does not execute commands or access data.]

## Skill Version(s):

2026.3.27 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
