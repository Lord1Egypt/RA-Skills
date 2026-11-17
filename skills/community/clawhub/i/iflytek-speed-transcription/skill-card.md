## Description:

Transcribes MP3 audio files to text using the iFLYTEK Speed Transcription API, with optional speaker separation, domain tuning, and text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to transcribe approved MP3 recordings through iFLYTEK/XFYun with optional speaker separation and domain-specific recognition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected MP3 audio and related metadata are uploaded to iFLYTEK/XFYun using XFEI credentials.

Mitigation: Use only recordings approved for that provider; avoid confidential, regulated, or non-consented audio unless policy allows.

Risk: Current implementation accepts MP3 files only despite broader format claims in the skill description.

Mitigation: Convert source audio to MP3 and verify the format before use.

Risk: The workflow depends on third-party API credentials, network access, and the Python requests dependency.

Mitigation: Configure XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET securely, and use a virtual environment with pinned dependencies where possible.

## Reference(s):

- [iFLYTEK Speed Transcription](https://www.xfyun.cn/services/speed_transcription)
- [iFLYTEK OST API Documentation](https://console.xfyun.cn/services/ost)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration guidance]

**Output Format:** [Plain text, JSON, or saved text/JSON files from command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task ID without polling when requested; default polling waits up to about 10 minutes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
