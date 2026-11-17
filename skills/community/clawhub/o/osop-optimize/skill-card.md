## Description:

Analyze .osoplog execution history to optimize workflows - finds slow steps and parallelization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archie0125](https://clawhub.ai/user/archie0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow authors use this skill to analyze OSOP execution logs, identify slow or unreliable nodes, and propose reliability and speed improvements. With user approval, it can update the selected .osop workflow after showing a diff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a selected .osop workflow and nearby execution logs, which may expose workflow details or execution history.

Mitigation: Install only when that access is acceptable, and run it in workspaces where the agent may inspect the relevant workflow and logs.

Risk: Optimization suggestions or approved edits could change workflow behavior.

Mitigation: Review the generated diff before approving any write to the .osop workflow.

## Reference(s):

- [OSOP](https://osop.ai)
- [ClawHub Skill Page](https://clawhub.ai/archie0125/skills/osop-optimize)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration]

**Output Format:** [Markdown suggestions table, workflow diff, and optional .osop configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a target .osop workflow path and access to nearby .osoplog.yaml execution logs.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
