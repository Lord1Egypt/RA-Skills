## Description:

Builds priority-based daily plans with breaks and a backlog, supports revisions and reviews, and exports schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People using an AI assistant can prioritize daily tasks, schedule realistic time blocks with breaks, track completion, carry open work forward, and export a plan for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details and exported plans remain in readable local workspace files.

Mitigation: Limit access to the active workspace and review exported files before sharing them.

Risk: Execution behavior and external setup services were not tested, and scanner code coverage was partial.

Mitigation: Use a reviewed CLI version when installing through npx and verify behavior in the intended workspace before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-daily-planner)
- [MochiLab](https://mochilab.bz)
- [Input contract](references/input.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, CSV]

**Output Format:** [Conversational planning guidance, daily-plan.md, and time-blocks.csv]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves task estimates and lists work that does not fit in the schedule as backlog; exports are saved in the active workspace.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
