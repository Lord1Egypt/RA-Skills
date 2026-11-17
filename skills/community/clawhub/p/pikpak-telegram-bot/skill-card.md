## Description:

Control PikPak from Telegram to save links, check transfer tasks, and receive notifications while retaining local state across restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External PikPak users use the skill to configure a Telegram bot that submits links to PikPak and checks transfer tasks or recent files. Real account and Telegram operations require explicit user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed bot token or untrusted PikPak CLI or Telegram API endpoint could put account access at risk.

Mitigation: Keep the token in a private environment, use a trusted PikPak CLI, and retain the default Telegram endpoint unless a replacement is trusted.

Risk: Incorrect chat or user allowlists can permit unauthorized control, and replies in groups are visible to group members.

Mitigation: Carefully configure both allowlists and use private chats for sensitive account information.

Risk: A submission with an uncertain result may already have been accepted, so an immediate retry can duplicate it.

Mitigation: Check the PikPak app manually before resending and retain the local state records.

## Reference(s):

- [Upstream design notes](artifact/references/upstream-design.md)
- [Telegram Bot API: getUpdates](https://core.telegram.org/bots/api#getupdates)
- [Telegram Bot API: Message](https://core.telegram.org/bots/api#message)
- [PikPak CLI help](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Text]

**Output Format:** [Markdown guidance, shell commands, and Telegram text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task lists show up to 15 active tasks; directory listings show the 10 most recent items.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
