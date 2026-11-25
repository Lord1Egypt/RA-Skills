## Description:

Stabilize shaky video (non-destructive stabilizer (smoothed camera path, border-hiding zoom, rolling-shutter correction)), solve 3D camera tracker anchors, track 2D regions/points with rotation and scale, and attach graphics or props to moving hands and objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and developers use this skill to stabilize footage, track regions and moving hands or objects, solve camera movement, and attach graphics to video scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Levea API key, which could be exposed if stored or shared insecurely.

Mitigation: Keep LEVEA_API_KEY in the plugin or MCP server's secret configuration and avoid sharing it in prompts or logs.

Risk: The security assessment is incomplete because one local reference was missing.

Mitigation: Review the missing reference and assess its relevance before relying on the skill.

## Reference(s):

- [Levea video editing service](https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=motion-tracking-stabilization)
- [ClawHub skill release](https://clawhub.ai/brajendrak00068/skills/motion-tracking-stabilization)

## Skill Output:

**Output Type(s):** [Video, JSON, Text]

**Output Format:** [Rendered MP4 video and structured edit status, project, verification, and quality information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a project ID and asynchronous job status before video export completes.]

## Skill Version(s):

1.0.3 (source: frontmatter; server release 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
