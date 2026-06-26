## Description: <br>
Guides an agent through OpenStatus CLI workflows for incidents, status reports, maintenance windows, monitor configuration, subscriber notifications, and status page lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openstatus](https://clawhub.ai/user/openstatus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to have an agent prepare or run OpenStatus CLI commands for live incident communication, maintenance scheduling, status page inspection, and monitor configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can create, update, resolve, or delete live incidents and maintenance windows on a status page. <br>
Mitigation: Require explicit user confirmation before running OpenStatus commands that change status-page data. <br>
Risk: Using --notify can email status page subscribers. <br>
Mitigation: Confirm notification intent and message content before running commands with --notify. <br>
Risk: The skill depends on OpenStatus authentication through login, access token flags, or OPENSTATUS_API_TOKEN. <br>
Mitigation: Use a scoped OpenStatus token where possible and avoid exposing token values in prompts, logs, or command output. <br>
Risk: The OpenStatus CLI must be installed locally before the skill can execute commands. <br>
Mitigation: Verify the CLI source and installation before using the skill for operational workflows. <br>


## Reference(s): <br>
- [OpenStatus official website](https://www.openstatus.dev) <br>
- [OpenStatus CLI repository](https://github.com/openstatusHQ/cli) <br>
- [Monitor Configuration Reference](references/monitor-config.md) <br>
- [ClawHub skill page](https://clawhub.ai/openstatus/openstatus) <br>
- [Publisher profile](https://clawhub.ai/user/openstatus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenStatus CLI commands, openstatus.yaml monitor examples, and confirmation guidance for live status-page changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
