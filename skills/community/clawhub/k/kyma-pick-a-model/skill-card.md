## Description:

Choose a model on Kyma API for a specific job by comparing real per-token price, measured 30-day uptime, and fit for the task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyma-api](https://clawhub.ai/user/kyma-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to choose Kyma API models for coding agents, chat, long-context, vision, reasoning, and cost-sensitive work. It compares live model availability, pricing, uptime, context window, tool support, and modality before recommending a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad model-selection questions and steer the answer toward Kyma API models outside an intended Kyma context.

Mitigation: Use the skill when Kyma API model selection or configuration is intended, and keep the trigger wording Kyma-specific during future revisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyma-api/skills/kyma-pick-a-model)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes one recommendation, one cheaper alternative, one stronger alternative, exact model IDs, prices, 30-day uptime figures, and configuration examples when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
