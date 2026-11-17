## Description:

OpenPet is a Tamagotchi-style virtual pet game for chat platforms where each user has a persistent pet that responds to care commands and evolves over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdealiaga](https://clawhub.ai/user/mdealiaga)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to add a persistent virtual pet game to chat platforms such as Discord, WhatsApp, and Telegram. It supports per-user pets, care commands, scheduled stat decay, alerts, and evolution over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps per-user pet files that include platform identifiers and owner metadata.

Mitigation: Limit access to the pet data directory, disclose what is stored, and provide a way to delete a user's pet data.

Risk: The scheduled decay task may continue running and send proactive chat alerts after installation.

Mitigation: Provide controls to pause or remove the cron job and let users opt out of proactive alerts.

Risk: The security review marks the release as suspicious because background behavior and user controls need review.

Mitigation: Install a pinned release only after reviewing the background task, alert behavior, and data deletion controls.

## Reference(s):

- [OpenPet README](README.md)
- [OpenPet configuration](references/config.json)
- [OpenPet sprites](references/sprites.json)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub OpenPet skill page](https://clawhub.ai/mdealiaga/skills/openpet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown chat responses with JSON state data and scheduled task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains per-user pet state and may send proactive chat alerts from a recurring decay task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
