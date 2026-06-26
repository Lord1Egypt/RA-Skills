## Description: <br>
使用科大讯飞 API 将音频/视频转换为文字。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and other external users can use this skill to transcribe local audio or downloaded YouTube audio with iFlytek cloud speech recognition, including Chinese dialect recognition and punctuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio submitted for transcription is sent to iFlytek's cloud service. <br>
Mitigation: Use only recordings that are authorized for cloud processing, avoid sensitive or regulated audio unless approved, and delete downloaded audio or transcripts when they are no longer needed. <br>
Risk: The skill relies on API credentials stored in a local .env file. <br>
Mitigation: Keep credentials private, exclude .env from version control and shared archives, and rotate credentials if they may have been exposed. <br>
Risk: The YouTube downloader path uses yt-dlp and includes an option that bypasses certificate checks. <br>
Mitigation: Review the downloader command before use, comply with source platform terms, and consider removing the certificate-bypass option in environments that require strict transport validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harven-droid/iflytek-asr) <br>
- [iFlytek Open Platform](https://www.xfyun.cn) <br>
- [iFlytek ASR documentation](https://www.xfyun.cn/doc/spark/asr_llm/Ifasr_llm.html) <br>
- [iFlytek Console](https://console.xfyun.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcripts and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local audio downloads and transcript files when scripts are executed by the agent or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
