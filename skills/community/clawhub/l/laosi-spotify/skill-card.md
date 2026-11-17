## Description:

Spotify控制技能 - 终端控制Spotify播放、搜索、管理播放列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to control Spotify from the terminal, including playback state, search, playlist actions, current-track display, and volume changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required dependency evidence names spotifyd and spotify-cli, while the artifact installation and examples use spicetify.

Mitigation: Confirm the intended Spotify CLI before installation and install it from a trusted source.

Risk: Broad trigger phrases and state-changing controls could change playback, playlists, or volume unexpectedly.

Mitigation: Require explicit user confirmation before playlist, playback, or volume changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-spotify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal commands that change Spotify playback, playlists, or volume.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
