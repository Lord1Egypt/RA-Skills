## Description:

Download media into /mnt/jellyfin_media subfolders and track progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivek9patel](https://clawhub.ai/user/vivek9patel)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a local media library use this skill to validate destination folders, download one or more media URLs into /mnt/jellyfin_media, and check download progress on demand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated URL input can turn a pasted link into command execution inside the skill runtime.

Mitigation: Review before installing, avoid untrusted or unusual URL strings, and prefer a version that validates http/https URLs and passes -- before yt-dlp URLs.

Risk: The skill writes downloaded media and progress state to mounted filesystem paths.

Mitigation: Run it in a constrained runtime with write access limited to the intended media directory and use a private state directory for progress files.

## Reference(s):

- [Media Sync on ClawHub](https://clawhub.ai/vivek9patel/skills/media-sync)
- [OpenClaw](https://openclaw.ai)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Jellyfin](https://jellyfin.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text status messages and structured tool reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create media files under /mnt/jellyfin_media and progress logs under /tmp.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
