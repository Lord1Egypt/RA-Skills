## Description: <br>
Provides voice transcription, multilingual audio handling, and message formatting to improve OpenClaw use in Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangshaoshuai123](https://clawhub.ai/user/huangshaoshuai123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers who work in Feishu can transcribe voice messages, normalize text replies, and save command output for downstream message handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice audio may be sent to Google Speech Recognition for transcription. <br>
Mitigation: Use only with user or administrator consent, and avoid sensitive or regulated audio unless the deployment has approved that data flow. <br>
Risk: Runtime behavior depends on Python packages and local audio conversion support. <br>
Mitigation: Review and pin SpeechRecognition and pydub dependencies before deployment, and test the supported audio formats in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangshaoshuai123/openclaw-feishu-optimizer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/huangshaoshuai123) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text, JSON files, and command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write recognition or message-processing results to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
