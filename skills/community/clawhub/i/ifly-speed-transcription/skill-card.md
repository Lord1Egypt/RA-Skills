## Description: <br>
Ultra-fast speech transcription using the iFLYTEK Speed Transcription API for MP3 audio up to 5 hours, with Chinese, English, Chinese dialect, and automatic language detection support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe MP3 audio through the iFLYTEK/XFYUN Speed Transcription API, including meetings, interviews, lectures, voice notes, call center recordings, legal proceedings, and medical consultations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files and multipart metadata may be sent to iFLYTEK/XFYUN for processing. <br>
Mitigation: Use the skill only for recordings that are approved for third-party processing, obtain required consent, and avoid confidential or regulated audio unless policy permits it. <br>
Risk: API credentials are required for use. <br>
Mitigation: Use scoped credentials through environment variables and rotate or revoke keys if exposure is suspected. <br>
Risk: The documentation mentions WAV/PCM, but the script currently accepts MP3 files only. <br>
Mitigation: Convert recordings to the documented MP3 requirements before use and do not rely on WAV/PCM support without reviewing the implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/ifly-speed-transcription) <br>
- [iFLYTEK Open Platform](https://www.xfyun.cn/) <br>
- [iFLYTEK Speed Transcription API documentation](https://console.xfyun.cn/services/ost) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON transcription results, with Markdown setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save transcription text or JSON to a local output file when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
