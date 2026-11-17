## Description:

Use this skill when an implementation plan needs batch execution with manual checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlreal](https://clawhub.ai/user/tlreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to execute implementation plan tasks in order, pause at defined checkpoints for human review, and finish with full verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow tells the agent to make commits while executing plan tasks, which may trigger repository automation or release processes.

Mitigation: Review the plan and checkpoint prompts before use, especially in repositories where commits have automation effects.

Risk: Batch execution can carry an incorrect plan assumption through several tasks before the next review point.

Mitigation: Use the documented checkpoints every 3-5 tasks, pause on uncertain design decisions or failed tests, and run the full test suite before finalizing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with checkpoint templates and inline commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to commit code during execution and to request human confirmation at checkpoints.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
