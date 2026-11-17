## Description:

Automatically discover and configure available Google Antigravity models and quotas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krnbwj](https://clawhub.ai/user/krnbwj)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to sync Google Antigravity model availability and quotas into openclaw.json, keeping the configured primary model valid when quotas or model availability change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an existing Google Antigravity OAuth session to query model availability.

Mitigation: Install and run it only in an OpenClaw environment where that OAuth session is intended for model discovery.

Risk: The skill rewrites OpenClaw model configuration and may change the primary model when the current model is unavailable or exhausted.

Mitigation: Review the selected primary model and compare openclaw.json with the generated backup after each sync.

Risk: A broad invocation such as a generic model update request could trigger configuration changes unexpectedly.

Mitigation: Invoke it with a specific request such as syncing Antigravity models.

Risk: If WhatsApp is configured without self-chat mode or an allowlist, the bot may accept messages from unintended senders.

Mitigation: Enable selfChatMode or configure allowFrom before exposing the WhatsApp channel.

## Reference(s):

- [OpenClaw Antigravity Sync Skill release](https://clawhub.ai/krnbwj/skills/openclaw-antigravity-sync)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal output and JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates openclaw.json and creates an openclaw.json.bak backup when run.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
