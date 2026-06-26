## Description: <br>
A video processing skill that uses FFmpeg to cut, convert, compress, extract frames or audio, replace audio, add text watermarks, and embed subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QiaoTuCodes](https://clawhub.ai/user/QiaoTuCodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to automate practical media processing tasks such as preparing videos for messaging limits, extracting screenshots or audio, converting formats, and adding watermarks or subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe metadata parsing could execute code when inspecting media files. <br>
Mitigation: Review or patch the parser before use, and avoid running the info command on untrusted media until numeric fraction parsing is strict. <br>
Risk: FFmpeg commands overwrite output files by default. <br>
Mitigation: Use explicit output paths in non-sensitive folders and avoid targeting existing files unless replacement is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QiaoTuCodes/openclaw-skill-cutmv-video-tool) <br>
- [FFmpeg documentation](https://ffmpeg.org/documentation.html) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, files, guidance] <br>
**Output Format:** [Python API calls or CLI commands that produce media files and JSON status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FFmpeg in PATH; output paths are user supplied and may overwrite existing files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
