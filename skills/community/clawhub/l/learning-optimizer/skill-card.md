## Description:

Learning optimizer - analyze study patterns, identify inefficiencies, suggest optimizations for better learning outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and students use this skill to analyze study schedules, identify learning inefficiencies, receive time allocation plans, and get focus-improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Study schedules, subjects, learning problems, and allocation inputs are saved locally by default.

Mitigation: Use LEARNING_OPTIMIZER_HOME to isolate data on shared machines, and delete local JSONL files when they are no longer needed.

## Reference(s):

- [Learning Optimizer on ClawHub](https://clawhub.ai/harrylabsj/skills/learning-optimizer)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Console text and JSON for local data-directory reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSONL logs for analysis, optimization, and allocation activity.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
