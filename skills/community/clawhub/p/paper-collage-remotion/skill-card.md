## Description:

Create, revise, or render layered paper-cutout / collage animations in Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to plan, build, validate, preview, and render layered paper-cutout video projects in Remotion from scripts, PNG assets, captions, and local audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and rendering use local npm and Remotion tooling with normal supply-chain exposure.

Mitigation: Install and render in a dedicated project directory or container, prefer pinned package versions, and use a reviewed lockfile.

Risk: Image utilities write files to caller-provided output paths, so careless prefixes or directories can create unwanted files.

Mitigation: Use filename-safe prefixes, review output directories before running sheet splitting, and keep generated assets inside the project workspace.

Risk: Invalid or missing assets can produce broken renders, clipped layers, or misleading video output.

Mitigation: Run the bundled project validator and review warnings for missing alpha channels, out-of-frame final positions, and incorrect scene metadata before rendering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/paper-collage-remotion)
- [README](README.md)
- [Skill Instructions](SKILL.md)
- [Remotion Starter](assets/remotion-starter/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, JSON configuration, and Remotion project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise local Remotion starter files, image-processing outputs, validation reports, still frames, and rendered video commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
