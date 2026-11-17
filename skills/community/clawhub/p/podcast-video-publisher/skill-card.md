## Description:

Render podcast episodes as 1080p art-slideshow MP4s and publish them to a YouTube Podcasts playlist: covers/thumbnails generated from your art, resumable batch upload, playlist ordering, retiring old versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and podcast operators use this skill to render episode audio and artwork into YouTube-ready MP4s, upload them, set thumbnails, assemble a podcast playlist, order episodes, and retire replaced videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores broad YouTube OAuth credentials that can modify channel and playlist state.

Mitigation: Use a dedicated YouTube channel or playlist, keep .youtube.json out of version control, and grant access only to accounts intended for this publishing workflow.

Risk: The publish pipeline can remove playlist items, reorder a public podcast playlist, and unlist replaced videos.

Mitigation: Before running playlist or retire phases, edit the playlist ID, review upload-state.json, back up current playlist contents, and confirm exactly which videos may be changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/podcast-video-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with script commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local MP4 and cover image files when the bundled scripts are run; upload progress is tracked in upload-state.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
