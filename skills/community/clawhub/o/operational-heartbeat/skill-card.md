## Description:

Automated daily health check for OpenClaw instances. Verifies memory file presence, detects stale/overdue cron jobs, and surfaces system status. Intended for scheduled execution via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumemaka](https://clawhub.ai/user/guillaumemaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a scheduled OpenClaw health check that ensures the daily memory file exists, reviews cron job status, and reports warnings or errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional memory-promotion step may read recent memory files that contain private or sensitive information.

Mitigation: Disable memory promotion by default or explicitly scope which memory files may be read before scheduled execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a daily memory file, summarize cron health, and recommend a non-zero exit when issues are found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
