## Description:

Switches the OpenClaw default model by backing up the configuration, updating `agents.defaults.model.primary`, restarting the gateway, and rolling back on restart failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lv-yezhen](https://clawhub.ai/user/lv-yezhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to change the default OpenClaw model through a guided workflow or standalone script while preserving a backup for rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change OpenClaw's default model and restart the gateway, interrupting the active session.

Mitigation: Use it only for explicit, trusted model-switch requests and schedule the gateway restart when interruption is acceptable.

Risk: The security review notes that the script does not provide the promised built-in validation that the target model is configured.

Mitigation: Verify the target model exists in the configured OpenClaw provider list before running the switch command.

Risk: Dry-run mode is not fully side-effect-free because it can create a backup file.

Mitigation: Tell users that dry-run may write a backup under the OpenClaw backup directory and remove unwanted backups after review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lv-yezhen/skills/openclaw-model-switcher)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an OpenClaw configuration backup and may restart the OpenClaw gateway when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
