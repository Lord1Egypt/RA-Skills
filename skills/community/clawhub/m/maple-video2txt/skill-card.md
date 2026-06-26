## Description: <br>
将本地视频或音频文件转写为 SRT 字幕文件和 TXT 纯文本文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chentx1243](https://clawhub.ai/user/Chentx1243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe local media into timestamped subtitles and plain-text transcripts for reviewing or understanding video and audio content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store plain-text transcripts of media content on the local filesystem. <br>
Mitigation: Choose output paths intentionally and avoid transcribing media whose transcript should not be stored locally. <br>
Risk: The first run may download Whisper model files and install or use local Python dependencies. <br>
Mitigation: Install only in an environment where local Python execution, package installation, and model downloads are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chentx1243/maple-video2txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [SRT subtitle files, TXT transcript files, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes transcript files to a chosen local output path and may download Whisper model files on first use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
