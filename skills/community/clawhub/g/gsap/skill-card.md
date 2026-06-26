## Description: <br>
GSAP animation reference for HyperFrames covering tween methods, easings, stagger, defaults, timelines, playback, and performance patterns for render-critical compositions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and motion engineers use this skill to write deterministic GSAP animations for HyperFrames compositions, including timeline setup, reusable effects, and optional audio visualization data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional audio extraction helper runs ffmpeg on user-provided media and writes JSON to a chosen path. <br>
Mitigation: Confirm ffmpeg and numpy are installed, choose input and output paths intentionally, and review generated audio-data JSON before embedding it. <br>
Risk: Sample HTML loads GSAP assets from external CDN URLs. <br>
Mitigation: Use the CDN only when it fits the deployment environment, or self-host and pin the required GSAP assets. <br>


## Reference(s): <br>
- [GSAP Effects for HyperFrames](references/effects.md) <br>
- [GSAP documentation](https://gsap.com/docs/v3/) <br>
- [GSAP Timeline pause documentation](https://gsap.com/docs/v3/GSAP/Timeline/pause%28%29/) <br>
- [ClawHub skill page](https://clawhub.ai/lucas-kay8/gsap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional helper script can produce audio-data JSON from user-selected local media.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
