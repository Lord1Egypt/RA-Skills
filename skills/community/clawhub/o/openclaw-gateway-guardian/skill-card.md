## Description: <br>
OpenClaw Gateway Guardian monitors an OpenClaw Gateway process and port, records health status, supports optional alerts, and attempts automatic restarts when the gateway repeatedly fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running OpenClaw Gateway use this skill to configure and operate a local watchdog for gateway availability. It helps detect repeated gateway failures, restart the service, and surface status through logs and optional notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a local watchdog process that restarts the OpenClaw gateway and leaves runtime files behind. <br>
Mitigation: Install it only when that behavior is intended, review the generated configuration, run with the least privileges needed, and document how to stop the watchdog and remove its runtime files. <br>
Risk: Deployment and notification setup can involve tokens, webhook URLs, or other credentials. <br>
Mitigation: Keep credentials out of repositories, command history, logs, screenshots, and shared configuration; prefer local secret storage or protected environment variables. <br>
Risk: Some artifact guidance includes token-in-URL Git examples and privileged or boot-start deployment patterns. <br>
Mitigation: Use safer authentication flows such as credential helpers or CLI login, review installers before execution, and avoid SYSTEM or boot-start deployment unless operationally required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/openclaw-gateway-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>
- [Project homepage](https://github.com/davidme6/openclaw-gateway-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local process-control commands, runtime file paths, and notification configuration guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
