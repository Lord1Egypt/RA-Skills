## Description:

Synchronize multi-camera podcast recordings by audio waveform and switch camera angles on the active speaker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast producers and editors use this skill to synchronize multiple camera and audio tracks, switch views to the active speaker, and assemble an edited episode through the Levea service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media is processed by the external Levea editing service, whose data-retention practices were not verified.

Mitigation: Use media you are comfortable sharing with Levea.

Risk: An exposed Levea API key could be misused.

Mitigation: Protect the API key in the plugin or MCP server configuration.

Risk: An automated edit may need review before it is applied.

Mitigation: Enable plan approval to review proposed edits first.

## Reference(s):

- [ClawHub release](https://clawhub.ai/brajendrak00068/skills/multicam-podcast-video-editor)
- [Levea editing service](https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=multicam-podcast-video-editor)

## Skill Output:

**Output Type(s):** [Text, Video files]

**Output Format:** [Structured edit status and project details, with an MP4 export URL when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports may complete asynchronously; reuse the project ID for follow-up edits.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
