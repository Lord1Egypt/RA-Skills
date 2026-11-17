## Description:

Helps plan multi-agent tasks by assigning roles and stating each agent's allowed and forbidden responsibilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to plan how multiple agents divide a large task, coordinate their work, and avoid overlapping responsibilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented CLI flags differ from those accepted by the included planner.

Mitigation: Check the script's --help output before automating it; use --task, optional --agents, and --json.

Risk: Broad multi-agent language may activate the skill when planning is not needed.

Mitigation: Confirm that the user wants an orchestration plan before applying its guidance.

Risk: Proposed role boundaries do not themselves enforce access control.

Mitigation: Review proposed roles and enforce permissions in the actual agent environment before execution.

## Reference(s):

- [Multi-Agent Conductor on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/multi-agent-conductor)
- [LGD theory referenced by the skill](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text role roster and allowed/forbidden boundaries, or structured JSON from the local planner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning guidance only; does not execute agents or enforce permissions]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter states 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
