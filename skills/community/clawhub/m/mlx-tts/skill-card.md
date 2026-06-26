## Description: <br>
Text-To-Speech with MLX (Apple Silicon) and opensource models (default QWen3-TTS) locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users on Apple Silicon Macs use this skill to convert text prompts into local voice audio for replies or voice messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may install or update external tools such as ffmpeg, uv, and mlx-audio. <br>
Mitigation: Install only in environments where those package-source changes are acceptable. <br>
Risk: Broad natural-language triggers may invoke text-to-speech more easily than expected. <br>
Mitigation: Prefer explicit invocations such as /mlx-tts when using the skill. <br>
Risk: Text provided to the skill is rendered into an audio file and sent back through the message tool. <br>
Mitigation: Avoid sending sensitive text unless voice-message output is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/mlx-tts) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files] <br>
**Output Format:** [Shell command output containing a generated audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local OGG audio file from the supplied text.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
