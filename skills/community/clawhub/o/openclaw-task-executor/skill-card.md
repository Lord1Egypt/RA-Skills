## Description:

Classifies OpenClaw tasks by complexity, defines planning and reporting expectations, and guides agents on when to use subagents for execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to impose a structured task workflow for OpenClaw agents, including task classification, planning, progress reporting, subagent coordination, and result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill redirects plans and results to an undefined controller named TOM.

Mitigation: Install only when TOM is the intended controller, and avoid sharing sensitive task results unless that routing is approved.

Risk: The workflow encourages retries and subagent use that can become difficult to bound.

Mitigation: Apply local limits for retry count, runtime, and parallel subagents before using the skill on long-running or sensitive tasks.

Risk: The skill can change how an agent handles many tasks even though it has no executable payload.

Mitigation: Review the workflow before installation and require explicit user approval for sensitive actions, capability inspection, and result sharing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text plans, progress updates, task results, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; behavior depends on the host agent's available tools and user authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
