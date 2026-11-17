## Description:

Design better OpenClaw HEARTBEAT.md files with adaptive cadence, safe checks, and cron handoffs for precise schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use Heartbeat to draft and tune HEARTBEAT.md files for adaptive monitoring, proactive check-ins, and cron handoffs for exact-time jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create or update heartbeat preferences, drafts, and snapshots under ~/heartbeat/.

Mitigation: Review the local file locations before use and keep generated heartbeat files scoped to the heartbeat workflow.

Risk: Example timezone and active-hour values may be copied into a live heartbeat file unchanged.

Mitigation: Replace the example Europe/Madrid timezone and sample active hours with the user's actual operating window before enabling proactive checks.

Risk: Cron handoff proposals can create scheduled jobs that run at exact times.

Mitigation: Review and explicitly approve any cron entries before allowing scheduled execution.

Risk: Overly broad monitors or ungated expensive checks can increase noise, token use, or paid API cost.

Mitigation: Use the documented cheap precheck gates, cooldowns, and scope limits before enabling expensive or frequent checks.

## Reference(s):

- [Heartbeat on ClawHub](https://clawhub.ai/ivangdavila/skills/heartbeat)
- [Heartbeat Homepage](https://clawic.com/skills/heartbeat)
- [OpenClaw Docs - Heartbeats](https://docs.openclaw.ai/advanced/heartbeats)
- [OpenClaw Docs - Cron vs Heartbeat](https://docs.openclaw.ai/advanced/cron-vs-heartbeat)
- [OpenClaw CLI System Skill](https://docs.openclaw.ai/openclaw-cli/system-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with heartbeat templates, checklists, and inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local heartbeat memory, draft, snapshot, and cron handoff files for user review.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
