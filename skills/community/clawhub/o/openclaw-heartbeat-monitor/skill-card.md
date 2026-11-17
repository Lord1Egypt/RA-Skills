## Description:

Heartbeat Monitor tracks freshness for recurring checks such as email, calendar, weather, and tasks, alerts when checks exceed configured thresholds, and generates health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent check whether recurring information refreshes are stale, prompt follow-up actions, and summarize heartbeat health across configured items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain a persistent local heartbeat state file that can become stale or inaccurate.

Mitigation: Review the state file location and configured thresholds, and periodically confirm that recorded check times match the agent's actual work.

Risk: Scheduling, reminders, or future automatic repair behavior could trigger checks or notifications outside the user's intended workflow.

Mitigation: Review any cron, reminder, or automatic repair implementation before enabling it, and keep automatic actions limited to explicitly approved check types.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangkai258/skills/openclaw-heartbeat-monitor)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status reports and reminder guidance with optional shell command examples and JSON configuration or state snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to the heartbeat state file at ~/.openclaw/workspace/memory/heartbeat-state.json and configurable interval thresholds.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, dated 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
