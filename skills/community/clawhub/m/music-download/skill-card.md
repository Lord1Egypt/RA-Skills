## Description:

Guides an agent through downloading MP3 music from NetEase Cloud Music and other supported platforms using yt-dlp, with you-get as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyang9317](https://clawhub.ai/user/ziyang9317)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare safe command-line downloads for individual songs, playlists, searches, and batch music downloads where the user is authorized to save the media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested yt-dlp installation method can affect system-managed Python packages.

Mitigation: Install yt-dlp in an isolated tool environment such as pipx or a virtual environment.

Risk: Batch downloads can place unexpected files in the target directory.

Mitigation: Review the download directory before and after batch downloads and use an explicit output path.

Risk: Downloading music may violate copyright or platform terms when the user lacks authorization.

Mitigation: Only download content the user is authorized to save and follow applicable copyright rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziyang9317/skills/music-download)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on user-provided music page, album, playlist, artist, or search URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
