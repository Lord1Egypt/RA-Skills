## Description: <br>
Switches the OpenClaw default model by validating a requested model, backing up openclaw.json, changing agents.defaults.model.primary, restarting the gateway, and rolling back on failure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lv-yezhen](https://clawhub.ai/user/lv-yezhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to switch the default model in an existing OpenClaw configuration while preserving a backup and attempting rollback if the gateway restart fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live OpenClaw configuration and affect gateway availability. <br>
Mitigation: Review the target model and exact agents.defaults.model.primary change before execution, require confirmation before gateway restart, and keep the generated backup available for rollback. <br>
Risk: Weak model validation could allow an unknown or unintended model name to be written. <br>
Mitigation: Only proceed after the requested model is matched against the configured provider list; if no clear match exists, stop and ask the user to choose from available models. <br>
Risk: Dry-run behavior may still create backup files. <br>
Mitigation: Treat dry run as potentially writing a backup unless the installed version has been verified to be fully side-effect-free. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lv-yezhen/openclaw-model-switcher) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit OpenClaw configuration, create backups, restart the gateway, and interrupt the active session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
