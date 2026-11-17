## Description:

Guides agents through generating original vocal songs from lyrics and style prompts using MiniMax Music 2.5 through Replicate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn structured lyrics and optional style direction into original vocal music for songs or music-video soundtracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested remote skill installs are unpinned and may change over time.

Mitigation: Review the referenced skills and pin trusted versions before installing.

Risk: Lyrics and prompts are processed by Replicate and MiniMax, and the API token may be exposed in shared logs.

Mitigation: Avoid sending sensitive or unreleased content unless third-party processing is acceptable, and keep the API token out of shared logs and transcripts.

## Reference(s):

- [music-2.5 skill release](https://clawhub.ai/pruna-ai/skills/music-2-5)
- [MiniMax Music 2.5 prediction endpoint](https://api.replicate.com/v1/models/minimax/music-2.5/predictions)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Audio]

**Output Format:** [Markdown with bash and JSON examples; downloadable audio from the model]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured lyrics and a Replicate API token; supports MP3, WAV, and PCM output.]

## Skill Version(s):

1.0.15 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
