## Description:

Automatically route tasks to the appropriate tool, agent, or workflow by analyzing task intent and complexity for coding, research, trading, system, or content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as a lightweight pre-processor that classifies incoming task descriptions and suggests an appropriate workflow or specialized agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword-based route classifications can be overbroad or incorrect, especially for trading and system-operation requests.

Mitigation: Use the route as advisory output and require separate confirmation before downstream agents execute trades, system commands, or other high-impact actions.

## Reference(s):

- [Task Router ClawHub listing](https://clawhub.ai/jimmyclanker/skills/jimmy-task-router)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route category, confidence score, reason, complexity, and suggested tool.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
