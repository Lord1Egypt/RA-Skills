## Description: <br>
Create video compositions, animations, title cards, overlays, captions, voiceovers, audio-reactive visuals, and scene transitions in HyperFrames HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative engineers use this skill to author HTML-based video compositions with timed scenes, motion, overlays, captions, voiceovers, and audio-reactive visual effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or modify project files while building HyperFrames compositions and design specifications. <br>
Mitigation: Review generated files and diffs before using them in production or committing them. <br>
Risk: The design picker workflow can start a local web server. <br>
Mitigation: Bind the server to 127.0.0.1, serve only the picker directory when possible, and stop the server promptly after use. <br>
Risk: Composition and picker workflows may load animation or font assets from third-party services. <br>
Mitigation: Review third-party asset URLs and replace them with approved local or vendor-approved assets when needed. <br>
Risk: Audio transcription workflows may upload audio to transcription APIs. <br>
Mitigation: Use approved transcription services only, and avoid sending sensitive audio unless policy permits it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucas-kay8/hyperframes) <br>
- [Video Composition](references/video-composition.md) <br>
- [Motion Principles](references/motion-principles.md) <br>
- [Design Picker](references/design-picker.md) <br>
- [Transcript Guide](references/transcript-guide.md) <br>
- [Transitions](references/transitions.md) <br>
- [GSAP CDN](https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project files, design.md specifications, HyperFrames composition HTML, animation code, captions, narration scripts, and local preview or render commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
