## Description: <br>
iaworker analyzes image, video, or camera input and produces step-by-step guidance for physical repair, debugging, assembly, and inspection tasks with optional spoken output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinleunglai](https://clawhub.ai/user/yinleunglai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use iaworker to turn images, videos, or live camera input into structured operating steps for repair, debugging, assembly, and inspection workflows. The skill is best treated as an assistant for guided task preparation and review, not as an authoritative visual diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated repair or diagnostic steps may be incomplete, generic, or incorrect for safety-critical physical tasks. <br>
Mitigation: Require human verification before acting on guidance, especially for vehicles, electrical systems, structural parts, or other hazardous work. <br>
Risk: Online text-to-speech may send spoken text to an external service when the default gTTS engine is used. <br>
Mitigation: Disable speech or configure offline TTS when guidance may include private, sensitive, or regulated details. <br>
Risk: Camera, image, and video analysis requires access to local media or live camera input. <br>
Mitigation: Use only media the operator is authorized to process and review local privacy expectations before enabling live camera workflows. <br>


## Reference(s): <br>
- [iaworker ClawHub release page](https://clawhub.ai/yinleunglai/iaworker) <br>
- [iaworker task guide](artifact/references/task-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, generated step objects, and optional audio playback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated steps to a Markdown file and may speak step summaries through TTS when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
