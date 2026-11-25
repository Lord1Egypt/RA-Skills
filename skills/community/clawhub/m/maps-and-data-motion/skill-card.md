## Description:

Builds animated travel maps, charts, counters, and audio visualizers from reusable presets for rendered videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and data storytellers use this skill to create rendered videos with animated maps and routes, charts, counters, or music visualizations using documented presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented `npx hyperframes` command may download and execute an unpinned package release.

Mitigation: Pin a reviewed HyperFrames version and inspect package and dependency changes before running it.

Risk: Security scan coverage is incomplete, including an unresolved local reference and an unscanned binary audio file.

Mitigation: Review unresolved references and inspect bundled binary assets before executing or redistributing the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vargai/skills/maps-and-data-motion)
- [Preset and source index](artifact/references/sources.md)
- [Vector route map guide](artifact/references/vector-route-map.md)
- [Self-drawing chart guide](artifact/references/self-drawing-chart.md)
- [Audio visualizer guide](artifact/references/audio-visualizer.md)
- [Natural Earth terms of use](https://www.naturalearthdata.com/about/terms-of-use/)
- [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/)
- [Web Audio API specification](https://webaudio.github.io/web-audio-api/)

## Skill Output:

**Output Type(s):** [Video files, Configuration, Code, Shell commands, Guidance]

**Output Format:** [MP4, WebM, or MOV video; JSON presets; code, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered video duration, resolution, frame rate, and transparency depend on the selected renderer and preset.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
