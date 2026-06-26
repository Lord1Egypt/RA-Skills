## Description: <br>
OpenClaw Rescue Kit helps agents guide local OpenClaw gateway operations, including startup wrapping, watchdog monitoring, automatic restart, configuration rollback, security hardening, log cleanup, and Git-based configuration versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m17y](https://clawhub.ai/user/m17y) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to install and operate a local OpenClaw maintenance kit for gateway health checks, restart handling, notification setup, configuration rollback, and log management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide installation of scripts that keep running in the background and make high-impact local changes. <br>
Mitigation: Review the scripts before enabling LaunchAgent or crontab jobs, use a dedicated gateway port, and keep unload or removal commands available. <br>
Risk: Notification and gateway configuration may involve local secrets such as webhook tokens. <br>
Mitigation: Protect ~/.openclaw/notify.conf and avoid committing webhook tokens or other secrets into local Git snapshots. <br>
Risk: Cleanup and rollback actions may alter local logs or configuration state. <br>
Mitigation: Test cleanup and rollback behavior on copies first, then save a known-safe configuration baseline before enabling automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m17y/openclaw-rescue-kit) <br>
- [OpenClaw complete guide](references/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for local scripts and background jobs; no structured API output.] <br>

## Skill Version(s): <br>
1.11.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
