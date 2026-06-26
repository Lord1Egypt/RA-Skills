## Description: <br>
Generate vertical short videos (9:16) from a Markdown script by parsing sections, generating TTS audio, rendering subtitle cards, and compositing MP4 output with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhedev](https://clawhub.ai/user/liuhedev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators can use this skill to turn structured Markdown video scripts into vertical short-form videos with synchronized narration, subtitle cards, and MP4 composition. It is intended for local media generation workflows that can provide FFmpeg, Chrome, and a TTS integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom TTS configuration exposes a broad local shell-command surface. <br>
Mitigation: Use the default TTS integration or a reviewed command you control; do not allow untrusted prompts, scripts, or agents to choose --tts-command. <br>
Risk: Untrusted Markdown content may be inserted into rendered HTML or JavaScript used for slide generation. <br>
Mitigation: Avoid processing untrusted Markdown until template escaping is improved, and review script text before rendering. <br>
Risk: The skill runs local media executables such as FFmpeg, ffprobe, Chrome, and TTS tooling. <br>
Mitigation: Install only in environments where local media processing tools are expected, and review generated files before publishing or relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liuhedev/lh-video-gen) <br>
- [Project homepage](https://github.com/liuhedev/lh-openclaw-kit) <br>
- [Script template](templates/script-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled generator produces MP4 video output and temporary PNG, HTML, MP3, and segment files during local execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
