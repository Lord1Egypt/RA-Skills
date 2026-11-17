## Description:

Leave or unassign from an accepted OpenAnt task and return it to the marketplace after the assigned worker confirms they want to abandon the assignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and external OpenAnt workers use this skill when they need to leave an assigned task, confirm the task state, and return the task to OPEN status without confusing worker unassignment with creator cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs authenticated task changes through an unpinned npm CLI package that can change after review.

Mitigation: Review before installing and prefer replacing @latest with a pinned, reviewed @openant-ai/cli version when operational control matters.

Risk: Unassigning a task is consequential because it reopens the task, affects the worker's reputation, and may prevent re-accepting the same task.

Mitigation: Confirm the task title, reward, assigned status, and user intent before running the unassign command.

Risk: Using the wrong workflow on a submitted task could disrupt payment or review.

Mitigation: Do not unassign submitted tasks; use the documented withdraw workflow only within the allowed revision window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ant-1984/skills/leave-task)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command snippets and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated OpenAnt CLI session and a task ID; the workflow requires --json output and explicit user confirmation before unassigning.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
