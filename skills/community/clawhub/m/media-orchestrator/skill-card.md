## Description:

Unified skill for resolving, downloading, and delivering media (audio/video) to chat platforms. Integrates yt-dlp for resolution and handles Spotify metadata sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieershafilone](https://clawhub.ai/user/sieershafilone)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to resolve media requests, download audio or video, synchronize Spotify metadata, and deliver the resulting media through WhatsApp or Telegram workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute local commands, download media, write workspace files, and send files or messages through configured chat accounts.

Mitigation: Review before installation, use only with controlled outbound recipients, and deploy in an environment where workspace file retention is acceptable.

Risk: Spotify handling depends on a separate spotify-surface component.

Mitigation: Install only when the spotify-surface dependency is trusted, reviewed, and pinned for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sieershafilone/skills/media-orchestrator)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Text]

**Output Format:** [Downloaded media files, Spotify metadata JSON, and chat delivery status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes media and metadata into the OpenClaw workspace and can send files or messages through configured WhatsApp or Telegram accounts.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
