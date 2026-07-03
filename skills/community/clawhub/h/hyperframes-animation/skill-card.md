## Description: <br>
Provides HyperFrames motion rules, scene blueprints, transitions, techniques, and runtime adapters for deterministic GSAP, Lottie, Three.js, Anime.js, CSS, Web Animations API, and TypeGPU animation work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heygen-com](https://clawhub.ai/user/heygen-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and motion designers use this skill to choose and compose HyperFrames animation recipes, scene blueprints, transitions, and runtime-specific patterns for deterministic rendered compositions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML examples may fetch CDN-hosted JavaScript libraries when opened or reused. <br>
Mitigation: Review examples before running them in restricted environments, and pin, vendor, or approve external animation libraries before production use. <br>
Risk: The animation-map helper can optionally bootstrap a helper package when dependencies are missing. <br>
Mitigation: Prefer preinstalling required helper packages or setting HYPERFRAMES_SKILL_PKG_VERSION explicitly; enable automatic bootstrap only after approving the shown npm package specification. <br>
Risk: Generated animation guidance can introduce incorrect timing, layout, or render-determinism issues in a target composition. <br>
Mitigation: Review generated code and run HyperFrames lint, validate, inspect, preview, or render checks before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heygen-com/skills/hyperframes-animation) <br>
- [HyperFrames animation rules index](artifact/rules-index.md) <br>
- [HyperFrames blueprints index](artifact/blueprints-index.md) <br>
- [HyperFrames transitions overview](artifact/transitions/overview.md) <br>
- [GSAP documentation](https://gsap.com/docs/v3/) <br>
- [Three.js WebGLRenderer documentation](https://threejs.org/docs/pages/WebGLRenderer.html) <br>
- [Anime.js documentation](https://animejs.com/documentation/) <br>
- [lottie-web](https://github.com/airbnb/lottie-web) <br>
- [MDN CSS animation documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation) <br>
- [MDN Web Animations API guide](https://developer.mozilla.org/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are proposals for HyperFrames animation authoring; generated code should be reviewed and tested in the target project.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
