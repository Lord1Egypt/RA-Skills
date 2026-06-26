## Description: <br>
Meeting Transcriber provides Chinese real-time meeting transcription with microphone capture, FunASR speech recognition, voice activity detection, automatic punctuation, saved transcript files, and environment checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinapjs](https://clawhub.ai/user/chinapjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who run OpenClaw on a local Windows workstation use this skill to start and stop Chinese meeting transcription, check the required Conda audio environment, and find saved meeting records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records microphone audio and may print or save sensitive meeting content locally. <br>
Mitigation: Get consent from meeting participants before use, avoid recording restricted conversations, and review saved transcripts before sharing or retaining them. <br>
Risk: The skill depends on a local Windows Conda setup and an external D:\dev\python\voiceFunAsr transcription script. <br>
Mitigation: Install only on trusted local machines, verify the external transcription script before running it, and confirm the audioProject Conda environment uses expected packages. <br>
Risk: The setup helper can create ~/.openclaw configuration and local support files. <br>
Mitigation: Run setup only when configuration changes are expected and review generated or modified files afterward. <br>


## Reference(s): <br>
- [Meeting Transcriber on ClawHub](https://clawhub.ai/chinapjs/meeting-transcriber) <br>
- [FunASR project](https://github.com/alibaba-damo-academy/FunASR) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal and OpenClaw text output with command suggestions, environment status, file paths, and saved transcript references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcripts are saved locally under the configured meeting_records directory when the external transcription script runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
