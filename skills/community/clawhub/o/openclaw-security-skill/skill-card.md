## Description: <br>
OpenClaw Security Configurator helps users check OpenClaw security posture, monitor token usage, and produce configuration and compliance guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2389275723](https://clawhub.ai/user/2389275723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and operations teams use this skill to review OpenClaw service status, local configuration, exposed ports, logs, and token usage before applying hardening or monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local service logs and may surface sensitive token, cost, API key, or configuration information. <br>
Mitigation: Review report and log output before sharing it, restrict generated files to trusted users, and avoid running checks in environments where secrets may be printed to shared terminals. <br>
Risk: The token monitor sources a local configuration file and can run as a background process with a PID file under /var/run. <br>
Mitigation: Inspect and lock down the configuration file before starting the monitor, run it with the least privileges available, and verify process ownership and stop behavior before enabling systemd integration. <br>
Risk: Webhook alerting can send operational information to an external destination. <br>
Mitigation: Use webhook alerts only with a trusted endpoint, keep webhook secrets out of shared files, and prefer log-only alerting until the destination and payload are reviewed. <br>
Risk: Some advertised payment, model-routing, and compliance capabilities are marketing claims rather than proven controls in the artifact. <br>
Mitigation: Treat those claims as unverified until implementation and audit evidence are available, and rely on the included scripts only for the checks they actually perform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2389275723/openclaw-security-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local text reports and monitoring logs when the bundled shell scripts are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
