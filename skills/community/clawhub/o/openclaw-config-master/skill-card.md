## Description: <br>
Helps agents edit and validate OpenClaw Gateway openclaw.json or JSON5 configuration across gateway, agents, channels, models, auth, tools, commands, sessions, hooks, secrets, plugins, skills, and includes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make schema-first OpenClaw Gateway configuration changes, validate openclaw.json or JSON5 files, migrate versions, and diagnose doctor or config validation errors without introducing invalid keys or weaker security policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration advice or patches could expose chat access through broad channel or group policies. <br>
Mitigation: Review every proposed patch before applying it and avoid open group policies unless that exposure is intentional. <br>
Risk: Diagnostics or examples could collect or reveal prompt, message, system-content, token, or API-key data. <br>
Mitigation: Keep prompt, message, and system-content diagnostics disabled except during short controlled debugging, and store secrets in environment variables or a secrets provider rather than in openclaw.json. <br>
Risk: Backup cleanup or restore operations can delete old backups or overwrite the active configuration. <br>
Mitigation: Preview backup deletion and restore operations before running them, keep a current backup, and avoid force options unless the target file and backup source are confirmed. <br>
Risk: Generated configuration changes can alter Gateway behavior or trigger restarts. <br>
Mitigation: Use schema lookup and validation first, then apply changes only after reviewing their security and operational impact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aqbjqtd/openclaw-config-master) <br>
- [OpenClaw configuration guide](https://docs.openclaw.ai/gateway/configuration) <br>
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference) <br>
- [OpenClaw Config CLI](https://docs.openclaw.ai/cli/config) <br>
- [OpenClaw Security CLI](https://docs.openclaw.ai/cli/security) <br>
- [Channels Configuration](references/channels-config.md) <br>
- [OpenClaw Config Field Index](references/openclaw-config-fields.md) <br>
- [Version Migration Guide](references/version-migration.md) <br>
- [Common Errors](references/common-errors.md) <br>
- [Complex Operations](references/complex-operations.md) <br>
- [Schema Sources](references/schema-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed OpenClaw config patches, validation steps, and backup or restore commands.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata; artifact _meta.json reports 1.3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
