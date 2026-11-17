## Description:

MISO provides Telegram-native mission control templates and helper commands for tracking OpenClaw multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunsukehayashi](https://clawhub.ai/user/shunsukehayashi)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to standardize Telegram mission-control updates for OpenClaw multi-agent work, including progress, approval gates, completion, and error states.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mission details may be shared automatically to fixed Telegram chats.

Mitigation: Review and replace channel destinations before use, and disable or gate channel auto-posting for confidential work.

Risk: Telegram bot credentials are used from local configuration.

Mitigation: Use a narrowly scoped Telegram bot credential, protect the local configuration file, and rotate the credential if it is exposed.

Risk: Mission state can persist locally in .miso-state.json.

Mitigation: Confirm retention expectations before deployment and clear the local state file when missions should no longer be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shunsukehayashi/skills/miso)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Design system](artifact/DESIGN-SYSTEM.md)
- [Channel integration](artifact/CHANNEL-INTEGRATION.md)
- [Spawn integration](artifact/SPAWN-INTEGRATION.md)
- [Master ticket state management](artifact/MASTER-TICKET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown templates with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram-oriented mission status templates, slash-command mappings, and bot helper command output.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
