## Description:

Helps agents create or continue a Vlog project in a local media workspace by reviewing footage and applying established photo, title, text-page, and sound workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milanor1970](https://clawhub.ai/user/milanor1970)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent operators use this skill to review local photos and video, plan and render story-driven Vlogs, and prepare covers and delivery notes in a project workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current Pillow dependency bound excludes a published fix for an image-processing security flaw.

Mitigation: Resolve the Pillow requirement and verify a patched build before processing images received from others.

Risk: Transferred workspaces may contain executable settings, and untrusted media tools can introduce risk.

Mitigation: Use trusted FFmpeg installations and inspect executable settings before using a transferred workspace.

Risk: Media indexes and transcripts can expose private content; agent viewing or optional online generation may send selected content to a configured service.

Mitigation: Keep indexes and transcripts private, and review what content is sent to any configured online service.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/milanor1970/skills/local-vlog-production)
- [First Run](references/first-run.md)
- [Visual Presets](references/visual-presets.md)
- [Validation](references/validation.md)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Rendered video and cover files, JSON timelines, Markdown project notes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local media workflow; footage review and final audio/video checks still require human judgment.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
