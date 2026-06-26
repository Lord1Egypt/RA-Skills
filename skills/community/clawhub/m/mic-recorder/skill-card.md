## Description: <br>
Mic Recorder guides agents through recording microphone audio on macOS with a user-created Automator app, denoising it with FFmpeg, and sending the processed WAV file to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tazio7](https://clawhub.ai/user/Tazio7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture voice or ambient audio on macOS, apply FFmpeg denoising, and send the resulting workspace audio file to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone recordings may capture people who have not consented. <br>
Mitigation: Use the skill only when all recorded parties know about and consent to the recording. <br>
Risk: Audio may be sent to the wrong Feishu destination. <br>
Mitigation: Verify the Feishu destination before sending any recording. <br>
Risk: Sensitive audio may be uploaded or retained longer than intended. <br>
Mitigation: Inspect recordings before upload and define how local and Feishu copies will be retained or deleted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tazio7/mic-recorder) <br>
- [Publisher profile](https://clawhub.ai/user/Tazio7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local recording paths, FFmpeg denoising commands, Automator usage steps, and Feishu send examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
