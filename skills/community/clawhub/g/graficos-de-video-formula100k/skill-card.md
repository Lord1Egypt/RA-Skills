## Description:

Converts a timed video transcript into scrapbook-style Formula 100K overlay concepts, generated PNG graphics, and a timing plan for video editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketing operators use this skill to turn timed Spanish video transcripts into scrapbook overlay concepts, generated PNG assets, and a practical superposition plan for editing reels or short videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript-derived prompts may be sent to a third-party image generator.

Mitigation: Use the skill only when the user is comfortable sending the transcript-derived prompt content to Higgsfield.

Risk: Generation consumes image credits and may create local output files.

Mitigation: Confirm total credit cost before generation and save generated PNGs only in the documented output folder.

Risk: The artifact includes local ffmpeg, ffprobe, and mlx-whisper steps that are not part of the OpenClaw server workflow.

Mitigation: For OpenClaw use, request a timed transcript from the user and treat local media-processing commands as reference-only guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/graficos-de-video-formula100k)
- [Publisher profile: formula100k](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown plan with prompt text, generated PNG files, and transcript notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 4 to 8 overlay graphics from timed transcripts and saves PNGs plus TRANSCRIPCION.md when image generation is available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
