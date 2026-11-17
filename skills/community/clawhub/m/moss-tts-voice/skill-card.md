## Description:

MOSS-TTS Voice helps agents generate text-to-speech audio, clone voices from reference audio, use preregistered voices, and convert outputs for messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luogao2333](https://clawhub.ai/user/luogao2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create MOSS Studio speech audio from text, optionally using a cloned or preregistered voice, and save the result in a channel-appropriate audio format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning and realtime synthesis upload text and voice samples to MOSS Studio.

Mitigation: Use only voices you own or have explicit permission to clone, avoid sensitive recordings, and install only if you trust MOSS Studio with the provided data.

Risk: The skill depends on MOSS_API_KEY for authenticated API access.

Mitigation: Store the API key in a secret manager or environment variable, avoid printing or committing it, and rotate it regularly.

Risk: Generated audio is written to temporary local files and converted with ffmpeg.

Mitigation: Review temporary-file handling, clean up generated files when no longer needed, and confirm ffmpeg is installed from a trusted source.

Risk: The Python dependency is specified as a broad requests version range.

Mitigation: Review and pin dependencies before production deployment.

## Reference(s):

- [MOSS Studio](https://studio.mosi.cn)
- [ClawHub Skill Page](https://clawhub.ai/luogao2333/skills/moss-tts-voice)
- [API Technical Guide](references/api-guide.md)
- [Channel Format Guide](references/channel-formats.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Audio files with optional JSON status output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio is saved as WAV, OGG, or MP3; OGG Opus is used for Feishu, Telegram, and WhatsApp voice-message workflows, while MP3 is used for Discord, Signal, and Slack file workflows.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
