## Description:

Strategic project manager that reads between the lines, expands scope intelligently, creates job postings, and routes to spawner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify ambiguous work, infer a concise set of missing tasks, plan dependency-aware execution waves, and route work to specialist agents. It is intended for session starts, post-agent handoffs, weak or missing next tickets, and blocker escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can infer additional work beyond the user's explicit request, including high-impact actions such as deploys, Git pushes, sub-agent work, and persistent project memory.

Mitigation: Require explicit approval before executing inferred or high-impact tasks, especially for repositories, deployments, outreach, payments, and account-connected workflows.

Risk: The skill creates and mutates workspace planning files and can route work to other agents, which may amplify incorrect scope or stale project assumptions.

Mitigation: Review generated job boards, NEXT_AGENT handoffs, risk-register updates, and persistent insights before relying on them for execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/orchestrator-pm)
- [ClawHub publisher profile](https://clawhub.ai/user/dodge1218)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown planning and routing files with concise handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates workspace planning artifacts such as JOB_BOARD.md, NEXT_AGENT.md, NEXT_TICKET.md, RISK_REGISTER.md, insights.md, and worklog.md; may route work to specialist or sub-agent skills.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
