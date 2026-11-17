## Description:

mp3-list-to-video helps agents merge MP3 files from a folder into an MP4 playlist video with either a black background or a tracklist menu with current-track highlighting and optional rotating vinyl visual effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecojust](https://clawhub.ai/user/ecojust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to batch-convert ordered MP3 playlists into MP4 files, optionally adding a readable song menu, current-track highlighting, preview frames, and vinyl-style motion for music compilation videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg commands may overwrite existing output or temporary files when paths are reused.

Mitigation: Choose output and temp paths deliberately and review generated file locations before execution.

Risk: Local processing can consume CPU, disk space, and create timeline files containing playlist filenames.

Mitigation: Run the skill only on media files intended for local processing and avoid sensitive filenames when generated artifacts may be shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecojust/skills/mp3-list-to-video)
- [Skill instructions](artifact/SKILL.md)
- [MP3 merge script](artifact/scripts/merge_playlist.py)
- [Playlist menu script](artifact/scripts/add_playlist_menu.py)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP4 playlist videos plus optional ASS subtitles, timeline JSON, PNG preview frames, frame plans, and intermediate visual assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
