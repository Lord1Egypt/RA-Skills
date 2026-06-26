## Description: <br>
Local ffmpeg-based video editing skill. Provides tested helpers for subtitles, background blur, color grading, two-pass loudness normalization, scene-detected highlight reels, vertical conversion for shorts, and clean audio-only extraction for transcription/podcast workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, editors, and content teams use this skill to run local ffmpeg workflows for subtitle formatting, clip extraction, highlight reels, color grading, loudness normalization, audio extraction, and vertical video conversion. It is useful when media should stay on the local machine and the agent should propose or run reproducible command-line editing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts read local media, transcript, LUT, and mask files selected by the user. <br>
Mitigation: Use only input files that are appropriate for local processing and avoid pointing the skill at unrelated private media or transcripts. <br>
Risk: The scripts can overwrite output paths chosen by the user. <br>
Mitigation: Choose explicit output filenames, keep originals separate from generated files, and review paths before running commands. <br>
Risk: Highlight reel processing writes temporary intermediate video clips under the system temp area. <br>
Mitigation: Run highlight reel workflows only on media suitable for temporary local storage and clean temp files according to local retention practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/openclaw-video-editor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and local media, subtitle, transcript, or configuration file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with ffmpeg, ffprobe, and python3; output files are written to user-selected paths.] <br>

## Skill Version(s): <br>
6.1.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
