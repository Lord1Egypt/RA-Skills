## Description: <br>
Switches OpenClaw heartbeat requests to a local Ollama model and installs a local guard that reverts unauthorized heartbeat configuration changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce cloud token usage by routing heartbeat checks to local Ollama and monitoring heartbeat configuration for unauthorized changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can install a user-level background guard that enforces the configured heartbeat model. <br>
Mitigation: Install only when persistent local enforcement is desired, review selected OpenClaw instances during setup, and use --uninstall to remove the guard. <br>
Risk: The skill modifies OpenClaw configuration and can revert later heartbeat model changes that are not reflected in the guard configuration. <br>
Mitigation: Keep generated backups and update heartbeat-guard.conf.json before intentionally changing heartbeat.model. <br>
Risk: The documented Linux Ollama installation path includes a curl-to-shell command. <br>
Mitigation: Prefer a trusted package manager or review the installer before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/heartbeat-ollama-guard) <br>
- [Publisher profile](https://clawhub.ai/user/halfmoon82) <br>
- [MIT-0 license](https://opensource.org/licenses/MIT-0) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with CLI commands and local configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install a user-level background guard and write OpenClaw configuration, backup, service, and log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, clawhub.yaml, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
