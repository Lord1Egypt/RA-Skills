## Description: <br>
Transcribes audio to text with Xiaomi MiMo-V2.5-ASR through a public Gradio API, supporting Chinese, English, and automatic language detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcchenx345](https://clawhub.ai/user/xcchenx345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert audio recordings into text transcripts, including Chinese, English, and auto-detected speech. It is useful when an agent needs to extract spoken content from common audio formats without running a local ASR model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio is uploaded to a cloud Hugging Face/Gradio service for transcription. <br>
Mitigation: Avoid confidential, regulated, or highly personal recordings unless the user understands the remote service's privacy and retention behavior. <br>
Risk: The security review reports that the skill disables HTTPS certificate verification. <br>
Mitigation: Use only after certificate verification is fixed, or limit use to non-sensitive recordings where that transport risk is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xcchenx345/mimo-asr) <br>
- [Xiaomi MiMo-V2.5-ASR Hugging Face Space](https://xiaomimimo-mimo-v2-5-asr.hf.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript or Markdown guidance with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the transcript to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
