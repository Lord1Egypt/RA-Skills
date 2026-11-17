## Description:

Muse Video helps agents plan video projects by producing pre-production materials such as scripts, storyboards, art direction, prompts, creative packages, and exportable planning documents; it is not an actual video rendering, compositing, image generation, or video generation skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojiangyong](https://clawhub.ai/user/luojiangyong)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, filmmakers, and agent users use this skill to turn a video idea or brief into structured pre-production outputs: creative direction, scripts, scene plans, storyboards, prompts, and export files for downstream production tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill understates optional AI-generation behavior.

Mitigation: Use it as a planning and export skill, and review any suggested handoff to image or video generation tools before acting on it.

Risk: The security guidance flags unsafe handling in generated HTML and XLSX exports when project content comes from untrusted briefs.

Mitigation: Avoid opening or sharing generated HTML and XLSX exports from untrusted inputs until HTML escaping and spreadsheet formula neutralization are confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luojiangyong/skills/muse-video-skill)
- [README](README.md)
- [Case Library Index](references/cases/INDEX.md)
- [Default Pipeline](references/pipelines/default.md)
- [Fast-Track Pipeline](references/pipelines/fast-track.md)
- [Project State Schema](assets/schemas/project-state.json)
- [Tool Selection Matrix](references/media/tool-matrix.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, JSON creative packages, HTML exports, Excel storyboard tables, and shell commands for local export scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally guide handoff to downstream image, video, audio, and HTML composition tools when those tools are configured.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
