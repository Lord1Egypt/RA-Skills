## Description: <br>
Installs and enables the Honcho OpenClaw plugin, runs interactive setup for API key configuration and optional legacy memory migration, and restarts the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajspig](https://clawhub.ai/user/ajspig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install Honcho-backed long-term memory, configure the Honcho endpoint, and migrate existing workspace memory files when they explicitly choose to do so. It is intended for workspaces where ongoing conversation memory and transmission to Honcho or a configured self-hosted endpoint are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can upload listed memory and configuration files to Honcho or a configured endpoint. <br>
Mitigation: Install only where that data transfer is acceptable, review the displayed file list and destination, and proceed only after explicit confirmation. <br>
Risk: After setup, the plugin can persistently observe conversations and transmit data across sessions. <br>
Mitigation: Disable the plugin with `openclaw plugins disable openclaw-honcho` when ongoing memory is no longer wanted. <br>
Risk: The Honcho API key is stored in OpenClaw configuration. <br>
Mitigation: Protect access to `~/.openclaw/openclaw.json` and rotate the Honcho API key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/ajspig/honcho-setup) <br>
- [Honcho Homepage](https://honcho.dev) <br>
- [Honcho App](https://app.honcho.dev) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw plugin installation, enablement, setup, restart, status, and disable commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
