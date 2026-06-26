## Description: <br>
OpenClaw 7x24 watchdog & auto-healer. Monitors gateway health, memory usage, zombie sessions, and disk space every 5 minutes with automatic restart when stuck. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and schedule a recurring OpenClaw watchdog that monitors gateway health, memory usage, zombie sessions, and disk space, then restarts the gateway when configured failure thresholds are hit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent automation that can restart the OpenClaw gateway automatically. <br>
Mitigation: Enable the cron job only when that behavior is intended, review the scheduled command before activation, and keep the disable or remove command available. <br>
Risk: The security review notes implementation mismatches around the broad Windows memory check and the actual log path. <br>
Mitigation: Review the script before deployment, fix or accept the Windows memory behavior, and confirm where logs are written in the target environment. <br>
Risk: Automatic restarts can interrupt active gateway work when thresholds are exceeded or responsiveness checks fail. <br>
Mitigation: Run the watchdog manually first, confirm thresholds match the deployment, and monitor the guardian log after enabling scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/guardian-auto-healer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron scheduling instructions and a Python watchdog script path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
