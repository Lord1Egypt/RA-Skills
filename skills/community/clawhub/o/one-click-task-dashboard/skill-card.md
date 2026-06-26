## Description: <br>
Generates and keeps refreshed a local task dashboard for OpenClaw cron jobs and macOS launchctl tasks, including index.html, data.json, and a localhost web service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williandong0305-max](https://clawhub.ai/user/williandong0305-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create a local dashboard that shows which OpenClaw and launchctl tasks have run, are pending, or have not run. It also supports local auto-refresh and a localhost HTTP service for ongoing task-status review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs persistent macOS LaunchAgents that refresh dashboard data and run a localhost web server. <br>
Mitigation: Run setup only on a trusted local machine, review the LaunchAgent labels before use, and unload or remove them when persistent refresh or local serving is no longer needed. <br>
Risk: The artifact includes optional ClawHub publishing automation and a retry job that can act on the user's ClawHub account. <br>
Mitigation: Do not run the publishing or publisher-retry scripts unless intentionally publishing this skill; if run unintentionally, remove the ai.x.publish-one-click-dashboard LaunchAgent and review ~/.openclaw logs. <br>
Risk: The dashboard may expose local task status and log-derived data through generated files and a localhost service. <br>
Mitigation: Keep the service bound to localhost, inspect generated data before sharing, and avoid exposing ~/.openclaw dashboard files outside the local machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williandong0305-max/one-click-task-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local HTML/JSON dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local dashboard files under ~/.openclaw/dashboard and may install macOS LaunchAgents for refresh and localhost serving.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
