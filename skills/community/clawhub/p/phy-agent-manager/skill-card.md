## Description:

Meta-orchestrator that analyzes complex multi-step tasks, recommends suitable subagents, and produces ready-to-execute phased plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify complex coding tasks, choose suitable subagents, and produce phased execution plans with checkpoints and follow-up prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer Codex into a subagent-planning workflow that may expand scope or choose unsuitable agents.

Mitigation: Review the generated plan before approving execution, especially agent choices, phase boundaries, and requested follow-up prompts.

Risk: Security-sensitive work may need specialized review before any proposed plan is executed.

Mitigation: Use the skill's security-review path for security-sensitive tasks and verify the plan before authorizing downstream execution.

## Reference(s):

- [Phy Agent Manager on ClawHub](https://clawhub.ai/phy041/skills/phy-agent-manager)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown execution plan with classification, phased tables, checkpoints, and prompt-style follow-up commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subagent recommendations and asks the user to approve, modify, or cancel the proposed plan before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
