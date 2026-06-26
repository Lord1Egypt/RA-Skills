## Description: <br>
Automates OpenClaw updates by checking installed versions, downloading the latest app release, updating the CLI, restarting the gateway, and logging the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmieting](https://clawhub.ai/user/jimmieting) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to keep a local OpenClaw CLI, macOS menu bar app, and gateway aligned with the latest release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater performs high-impact local changes, including replacing the installed OpenClaw app, globally updating the CLI, and restarting the gateway. <br>
Mitigation: Review the script and target version before running it, use it during an acceptable maintenance window, and keep a rollback path available. <br>
Risk: The update flow depends on the publisher and the OpenClaw GitHub and npm release channels. <br>
Mitigation: Run it only when you trust those sources, and confirm the intended OpenClaw release and package source before execution. <br>


## Reference(s): <br>
- [Openclaw Autoupdate on ClawHub](https://clawhub.ai/jimmieting/openclaw-autoupdate) <br>
- [OpenClaw latest release API](https://api.github.com/repos/openclaw/openclaw/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions and shell execution logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes update logs to ~/.openclaw/logs/autoupdate.log and may replace the OpenClaw app, update the global CLI, and restart the gateway.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
