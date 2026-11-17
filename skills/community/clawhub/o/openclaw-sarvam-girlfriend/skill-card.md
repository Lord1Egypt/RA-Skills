## Description:

Rupali generates short, playful Indian-English virtual girlfriend replies and returns them as Bulbul v3 MP3 audio for chat channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altonappleton32-ux](https://clawhub.ai/user/altonappleton32-ux)

### License/Terms of Use:


## Use Case:

External users and chat-bot operators use this skill to create brief, friendly companion-style replies and deliver them as audio attachments in Discord, Telegram, or WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reply text is sent to Sarvam's TTS API using SARVAM_API_KEY.

Mitigation: Use only when third-party text-to-speech processing is acceptable; avoid highly private or sensitive conversations.

Risk: MP3 files are returned in the requesting chat channel.

Mitigation: Confirm the channel is appropriate before sending generated audio attachments.

Risk: The romantic entertainment persona could drift toward exclusivity, dependency, or explicit content.

Mitigation: Keep replies fictional, PG-13, brief, and avoid exclusivity, guilt, dependency cues, or explicit content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/altonappleton32-ux/skills/openclaw-sarvam-girlfriend)
- [Sarvam text-to-speech API endpoint](https://api.sarvam.ai/text-to-speech/stream)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Short text reply plus MP3 audio file attachment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses speaker rupali, default Indian English language settings, and SARVAM_API_KEY for text-to-speech synthesis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
