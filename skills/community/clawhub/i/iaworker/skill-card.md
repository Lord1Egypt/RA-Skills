## Description:

Intelligent Automation Worker analyzes image, video, or live camera inputs and generates structured physical-task guidance with optional visual and TTS delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinleunglai](https://clawhub.ai/user/yinleunglai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect physical-task inputs, draft step-by-step repair, debugging, assembly, or inspection guidance, and optionally deliver those steps through terminal markdown and speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate visual diagnosis reliability while producing physical repair or inspection guidance.

Mitigation: Treat generated diagnosis and repair steps as generic guidance, verify observations manually, and require expert review for vehicle, electrical, structural, or other high-risk work.

Risk: Spoken output defaults to an online TTS service, which can expose task details to a third-party service.

Mitigation: Disable speech or switch TTS to the offline pyttsx3 engine before handling sensitive images, videos, locations, equipment details, or user information.

## Reference(s):

- [iaworker ClawHub skill page](https://clawhub.ai/yinleunglai/skills/iaworker)
- [yinleunglai ClawHub publisher profile](https://clawhub.ai/user/yinleunglai)
- [Task guide](references/task-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with structured numbered steps, optional saved markdown files, and optional spoken TTS delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [TTS is enabled in configuration and defaults to online gTTS with offline pyttsx3 available as an alternative.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
