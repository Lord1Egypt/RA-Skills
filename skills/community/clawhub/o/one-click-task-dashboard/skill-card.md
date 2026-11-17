## Description:

Creates a local dashboard for OpenClaw cron jobs and macOS launchctl tasks, generating index.html and data.json with auto-refresh and a localhost web service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williandong0305-max](https://clawhub.ai/user/williandong0305-max)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect OpenClaw cron jobs and macOS launchctl task status in a local dashboard, including recent run state, schedules, summaries, and metrics. It is most relevant for macOS environments where LaunchAgents are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard setup installs persistent macOS LaunchAgents and serves task data from ~/.openclaw/dashboard on localhost.

Mitigation: Run setup only on intended macOS accounts, review the LaunchAgent files before installation, and remove the dashboard LaunchAgents when no longer needed.

Risk: Dashboard data can include task names, schedules, summaries, and metrics written to local HTML and JSON files.

Mitigation: Inspect generated data before sharing the machine, browser session, or dashboard directory, and keep the service bound to localhost.

Risk: The artifact includes account-linked ClawHub publishing and persistent retry automation that does not fit the dashboard purpose.

Mitigation: Do not run publish_to_clawhub.sh, publish_retry.sh, or setup_publisher_retry.sh unless intentionally publishing from the active ClawHub account; review or remove those scripts first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williandong0305-max/skills/one-click-task-dashboard)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated dashboard files are HTML and JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local files under ~/.openclaw/dashboard and can install macOS LaunchAgents for refresh and localhost serving.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
