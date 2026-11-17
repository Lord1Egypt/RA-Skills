## Description:

Ghostty helps an agent monitor communication channels, build a voice profile from sent messages, draft replies in the user's style, and route responses through approval or escalation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Ghostty to configure an always-on communication assistant that monitors email, calendar, Slack, WhatsApp, Signal, and Telegram, then drafts and routes replies in the user's voice. The skill is intended for personal communication management workflows that require strong approval, credential, and privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad, persistent access to private communications across multiple channels.

Mitigation: Limit each channel integration to the minimum required scopes, keep credentials in a secret manager or OS keychain, and review access before enabling continuous monitors.

Risk: The skill can send messages or accept calendar invitations as the user when direct-send or priority-sender rules are enabled.

Mitigation: Require explicit approval for every outbound message and calendar change unless the user has intentionally enabled a narrow, audited exception.

Risk: The voice profile is derived from private message exports and may become persistent communication-derived data.

Mitigation: Use only message samples the user is comfortable processing, store generated profiles outside shared workspaces, and delete or rotate profiles when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/ghostty)
- [Voice Profile](references/voice-profile.md)
- [Channel Monitors](references/channel-monitors.md)
- [Draft Engine](references/draft-engine.md)
- [Delivery Router](references/delivery-router.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated voice-profile markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration, draft queues, sent logs, and voice-profile files when followed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
