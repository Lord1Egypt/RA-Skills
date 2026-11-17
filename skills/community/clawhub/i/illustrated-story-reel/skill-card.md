## Description:

Creates illustrated slideshow stories with narration or music and gentle Ken Burns or optional generated motion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to plan and produce illustrated story reels with per-scene stills, narration or music, and an assembled video. It requests approval between generation stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned installation commands may fetch untrusted or changed skill code.

Mitigation: Use a trusted or version-pinned skills CLI rather than blindly running unpinned npx commands.

Risk: Prompts and uploaded media are sent to Pruna or Replicate during generation.

Mitigation: Avoid sensitive inputs and confirm the content is appropriate to send to those services.

Risk: Video assembly overwrites the target MP4, and generated plans or media may contain sensitive content.

Mitigation: Confirm a non-sensitive output directory and filename before assembly; protect generated project files.

Risk: Image, audio, and optional video generation can incur paid API usage.

Mitigation: Review the plan and approve each staged generation step before proceeding.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pruna-ai/skills/illustrated-story-reel)
- [API reference](artifact/references/illustrated-story-reel-api.md)
- [Approval gates](artifact/references/illustrated-story-reel-gates.md)
- [Motion guidance](artifact/references/illustrated-story-reel-p-video-motion.md)
- [Prompt guidance](artifact/references/illustrated-story-reel-prompts.md)
- [Quality checks](artifact/references/illustrated-story-reel-quality.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON plans, Shell commands, Media files]

**Output Format:** [Markdown guidance, JSON plans, and an MP4 story reel with image and audio assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User approval gates separate stills, audio, optional video clips, and final assembly.]

## Skill Version(s):

1.0.15 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
