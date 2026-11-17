## Description:

Audit and optimize OpenClaw token usage, cron job efficiency, and agent performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrmps](https://clawhub.ai/user/mrmps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw cron jobs, trace expensive agent runs, calculate token usage, and propose approved changes that reduce cost or improve reliability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local OpenClaw configuration, session traces, logs, or transcripts.

Mitigation: Confirm the specific job or session before trace analysis, avoid exposing raw transcripts or config values in reports, and summarize findings at the minimum detail needed.

Risk: Cron deletion, cron edits, and gateway restarts can disrupt scheduled automation.

Mitigation: Require explicit user approval for each operational change, record the baseline and intended rollback, and verify behavior after several runs.

Risk: Optimization recommendations could reduce context, change schedules, or alter models in ways that affect task quality.

Mitigation: Present projected impact before changes, preserve mission-critical jobs when the user identifies them, and compare before-and-after token usage and output quality.

## Reference(s):

- [OpenClaw cron jobs documentation](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenClaw CLI reference](https://docs.openclaw.ai/cli)
- [OpenClaw CLI cron reference](https://docs.openclaw.ai/cli/cron)
- [OpenClaw gateway security documentation](https://docs.openclaw.ai/gateway/security)
- [ClawHub skill page](https://clawhub.ai/mrmps/skills/openclaw-optimize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive recommendations require explicit user approval before applying operational changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
