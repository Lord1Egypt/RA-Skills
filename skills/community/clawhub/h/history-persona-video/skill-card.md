## Description:

Guides an agent through creating 45-60 second vertical AI restoration videos of historical figures, including source research, image generation, narration, music, title cards, ffmpeg assembly, validation, and delivery notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chugenice](https://clawhub.ai/user/chugenice)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to plan and assemble short-form historical-persona videos with AI-generated portraits, TTS narration, background music, cards, subtitles, and quality checks. The workflow is intended for artistic reconstruction and requires a disclaimer that outputs are not real photographs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled RunningHub client can run broad paid media-generation workflows beyond the narrow historical-video recipe.

Mitigation: Install only when that broad media-client access is intended, use a limited personal RunningHub API key, and monitor balance usage.

Risk: Local media may be uploaded to RunningHub during image, audio, video, or AI application workflows.

Mitigation: Avoid using private or sensitive media unless the user is comfortable sending it to RunningHub.

Risk: API-key handling is called out by security guidance as risky.

Mitigation: Use only the installer's own API key, do not share or embed keys, rotate exposed keys, and prefer narrowed key storage and transmission before treating the release as low risk.

Risk: Voice cloning or generated narration could be misused without consent.

Mitigation: Do not use voice cloning unless the voice owner has clearly consented.

Risk: AI historical reconstructions may be mistaken for authentic photographs or factual evidence.

Mitigation: Include the skill's artistic-reconstruction disclaimer with each delivered video.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/chugenice/history-persona-video)
- [ClawHub skill page](https://clawhub.ai/chugenice/skills/history-persona-video)
- [Target skill instructions](artifact/SKILL.md)
- [Target README](artifact/README.md)
- [RunningHub API key setup](artifact/skills/runninghub/references/api-key-setup.md)
- [RunningHub video model workflow](artifact/skills/runninghub/references/video-models.md)
- [RunningHub image model workflow](artifact/skills/runninghub/references/image-models.md)
- [RunningHub output delivery](artifact/skills/runninghub/references/output-delivery.md)
- [RunningHub service](https://www.runninghub.cn)
- [Wikimedia Commons file retrieval pattern](https://commons.wikimedia.org/wiki/Special:FilePath/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and expected media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local images, audio, and MP4 video assets through ffmpeg and RunningHub-backed generation workflows; outputs should include duration, resolution, voice, font, cost, and an artistic-reconstruction disclaimer.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
