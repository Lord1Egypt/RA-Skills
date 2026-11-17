## Description:

GSAP animation reference for HyperFrames. Covers gsap.to(), from(), fromTo(), easing, stagger, defaults, timelines (gsap.timeline(), position parameter, labels, nesting, playback), and performance (transforms, will-change, quickTo). Use when writing GSAP animations in HyperFrames compositions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to write deterministic GSAP animations for HyperFrames compositions, including tweens, timelines, transform-friendly motion, typewriter effects, and audio visualizers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audio visualizer helper can consume excessive local resources when run with extreme frame-rate, band-count, or media-size settings.

Mitigation: Run the helper manually on trusted media and keep fps and band counts reasonable.

Risk: Example animations may include CDN-hosted GSAP scripts that do not match every project policy.

Mitigation: Review CDN script usage against the target project's dependency and security policy before adopting the examples.

## Reference(s):

- [GSAP Effects for HyperFrames](references/effects.md)
- [GSAP documentation](https://gsap.com/docs/v3/)
- [GSAP Timeline pause documentation](https://gsap.com/docs/v3/GSAP/Timeline/pause%28%29/)
- [ClawHub skill page](https://clawhub.ai/lucas-kay8/skills/gsap)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose use of the bundled audio extraction helper, which produces per-frame JSON audio visualization data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
