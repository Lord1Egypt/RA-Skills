## Description: <br>
Jarvis-Video-STT helps agents batch-transcribe local video files with Faster-Whisper and produce subtitles, text transcripts, and summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to transcribe batches of local videos into SRT subtitles, plain text transcripts, and processing reports for review, search, or content preprocessing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell command construction when invoking ffmpeg may execute unintended commands for crafted video filenames. <br>
Mitigation: Process only trusted local video files with ordinary filenames until the script is changed to call ffmpeg through subprocess with an argument list. <br>
Risk: Generated transcripts and reports may contain confidential recording content saved in the local output folder. <br>
Mitigation: Use a dedicated output directory and avoid confidential recordings unless local transcript storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/jarvis-video-stt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated artifacts include SRT, TXT, JSON, and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local faster-whisper, tqdm, and ffmpeg dependencies; writes transcription outputs to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
