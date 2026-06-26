## Description: <br>
Use PM2 to reliably restart an OpenClaw gateway on Windows, recover from crashes, and handle port or startup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zitao666](https://clawhub.ai/user/zitao666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to restart or recover a Windows OpenClaw gateway managed by PM2, including checking status and resolving common port or startup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restart commands can briefly interrupt gateway availability or affect the wrong PM2 process if names, paths, or ports are incorrect. <br>
Mitigation: Confirm the PM2 process name, Windows paths, and port before running commands, and restart only when a brief gateway outage is acceptable. <br>
Risk: Setup commands install PM2 globally and configure a persistent gateway process. <br>
Mitigation: Run setup only when PM2 should manage the OpenClaw gateway, and review the command paths before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume PM2 manages the OpenClaw gateway on Windows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
