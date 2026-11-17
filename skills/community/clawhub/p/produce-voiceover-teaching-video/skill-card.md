## Description:

Turn a supplied narration audio file plus an article, notes, screenshots, images, or source videos into a fact-checked faceless vertical teaching video, synchronized captions, cover, publish copy, hashtags, and pinned comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuq87573-create](https://clawhub.ai/user/fuq87573-create)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and agent operators use this skill to turn supplied narration and local source assets into a vertical teaching video package. It coordinates intake, timing, storyboard, visual preparation, composition, QC, cover creation, and publishing copy while keeping user media scoped to the selected job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied narration and media may contain private or rights-sensitive material.

Mitigation: Run jobs in a per-job directory, provide only the intended source files, and confirm article, screenshot, voice, music, font, and logo rights before public release.

Risk: Publishing outputs could expose media or account destinations if treated as automatically approved.

Mitigation: Publish only after explicit user authorization for the destination and account; otherwise deliver local video, cover, QC, and copy artifacts only.

Risk: The bundled cover template favors Simplified Chinese styling by default.

Mitigation: Review or modify cover styling and exact text for the target audience before publishing.

## Reference(s):

- [Artifact contracts](references/contracts.md)
- [Seven-worker workflow](references/workflow.md)
- [Performance modes](references/performance.md)
- [Cover and publishing outputs](references/publishing.md)
- [ClawHub skill page](https://clawhub.ai/fuq87573-create/skills/produce-voiceover-teaching-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON stage reports, shell commands, generated media files, cover image, and publishing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local job directory with final.mp4, cover.png, publish-copy.json, subtitles, QC reports, and intermediate JSON handoffs.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
