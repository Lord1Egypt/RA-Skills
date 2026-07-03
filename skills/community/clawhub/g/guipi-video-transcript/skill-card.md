## Description: <br>
从本地视频文件中提取语音文案和字幕，在用户提供视频路径后生成转写文本、SRT 字幕和音频文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and content creators use this skill to extract spoken copy, plain text transcripts, SRT subtitles, and reusable audio from local video files for editing, review, or repurposing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the release as suspicious because the transcription workflow can require first-run internet access, automatic Python package installation, and model downloads despite presenting itself as offline after setup. <br>
Mitigation: Review and approve dependency installation and model downloads before use; prefer pinned dependencies, documented side effects, and verified model files. <br>
Risk: The artifact writes model cache and skill state under the user's home directory and may add promotional output after transcription. <br>
Mitigation: Run in a controlled workspace, review generated files and home-directory state, and disable or remove promotional output where it is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guipi888/guipi-video-transcript) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/guipi888) <br>
- [whisper.cpp Model Files](https://huggingface.co/ggerganov/whisper.cpp) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated TXT, SRT, and WAV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local transcript, subtitle, audio, and state files in user-specified or home-directory paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
