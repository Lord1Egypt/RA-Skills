## Description:

Visual cron job dashboard for OpenClaw — live countdown timers, run history, calendar view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firstfloris](https://clawhub.ai/user/firstfloris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to deploy and view a cron job dashboard with live countdowns, run history, and calendar views for jobs stored in OpenClaw cron files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron job names, schedules, prompts, run history, errors, and related metadata may be embedded into dashboard files or served by an unauthenticated local web server.

Mitigation: Review the code before installation, bind the server to localhost only, add authentication where appropriate, and avoid exposing the dashboard beyond trusted users.

Risk: The dashboard uses mutable remote HTML paths.

Mitigation: Pin or vendor the dashboard HTML before use and review updates before deployment.

Risk: Automatic post-run startup and link behavior can make the dashboard easier to expose unintentionally.

Mitigation: Remove or limit automatic post-run startup and link output unless that exposure is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firstfloris/skills/opencron)
- [OpenCron dashboard repository](https://github.com/firstfloris/opencron)
- [OpenCron dashboard HTML template](https://raw.githubusercontent.com/firstfloris/opencron/master/cron-dashboard.html)
- [Dashboard overview image](https://raw.githubusercontent.com/firstfloris/opencron/master/docs/overview.png)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local dashboard URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local HTTP dashboard server and generate or update embedded HTML dashboard files.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
