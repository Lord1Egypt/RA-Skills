## Description: <br>
mp3-list-to-video helps an agent combine MP3 files from a playlist folder into an MP4 video, with either a black background or a track-list menu that highlights the current song and can include a rotating vinyl animation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecojust](https://clawhub.ai/user/ecojust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn ordered local MP3 playlists into shareable MP4 compilation videos and menu-highlight variants for review or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite media and temporary files in configured output locations. <br>
Mitigation: Run it in a dedicated workspace and set explicit playlist, output, and temp paths before execution. <br>
Risk: The skill invokes local Python scripts and ffmpeg/ffprobe to process local MP3 files. <br>
Mitigation: Use trusted local audio files and a trusted FFmpeg installation, then review the generated preview frames and output paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ecojust/mp3-list-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts can create local MP4 videos, preview PNGs, ASS subtitle layers, timeline JSON, and temporary rendering files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
