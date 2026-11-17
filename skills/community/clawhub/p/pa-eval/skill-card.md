## Description:

Evaluate PA performance through structured scoring, owner feedback analysis, and behavioral benchmarking for weekly and monthly reviews, response quality assessment, and improvement planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Personal assistants and their owners use this skill to score PA execution, accuracy, speed, proactivity, communication, memory, tool use, and judgment. It supports weekly self-evaluations, owner-feedback follow-up, monthly reporting, and behavior benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistent logging can record sensitive feedback and behavioral judgments.

Mitigation: Use the skill only with explicit schedules and consent, and periodically review or delete .learnings/eval records that contain sensitive feedback.

Risk: Automated scoring may overstate performance patterns if owner feedback is incomplete or ambiguous.

Mitigation: Review generated scores and notes before using them for decisions, especially after corrections or complaints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/netanel-abergel/skills/pa-eval)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Analysis, Guidance]

**Output Format:** [Markdown templates and reports with optional shell commands for local file creation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local evaluation notes under a .learnings/eval path when the file-creation workflow is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
