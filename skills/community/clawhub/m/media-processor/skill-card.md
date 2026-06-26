## Description: <br>
Media Processor supports audio and video conversion, editing, extraction, and transcription workflows for multimedia content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media engineers use this skill to guide and support local multimedia processing tasks such as transcoding, clipping, audio processing, subtitle generation, and speech-to-text transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media-processing operations can overwrite local files when outputs point at existing files or shared workspaces. <br>
Mitigation: Use explicit output folders, avoid existing output filenames, and prefer versions that refuse to overwrite unless the user explicitly requests it. <br>
Risk: Unpinned dependency ranges and external media tooling can introduce environment drift. <br>
Mitigation: Pin and review dependency versions, verify the FFmpeg installation, and run the skill in a controlled workspace before using valuable media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/media-processor) <br>
- [Media Processor homepage](https://github.com/openclaw/media-processor) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local media output files at user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
