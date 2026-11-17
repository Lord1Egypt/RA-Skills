## Description:

Generates multi-voice movie and TV recap voiceovers, SRT subtitles, and per-line timing from scripts using the Miragea API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghhu](https://clawhub.ai/user/yanghhu)

### License/Terms of Use:

MIT

## Use Case:

Video creators and editing teams use this skill to turn movie, TV, short drama, anime, or documentary scripts into multi-voice narration with subtitles and line timings for editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can reproduce an identifiable person's voice.

Mitigation: Use only your own voice or a voice for which you have explicit authorization; do not imitate people without permission.

Risk: An API timeout may occur while a generation task is still running.

Mitigation: Check the task with the task or wait command, or retry with the same idempotency key to retrieve the existing task.

Risk: The security review notes workflow and tool-scope concerns and says its scan was partial.

Mitigation: Review the intended tool scope and the relevant referenced files before running the workflow.

## Reference(s):

- [Miragea](https://miragea.ai)
- [Miragea API](https://miragea.ai/v1)
- [Miragea API key setup](https://miragea.ai/workspace/api)
- [ClawHub skill release](https://clawhub.ai/yanghhu/skills/movie-recap-voiceover)

## Skill Output:

**Output Type(s):** [Audio files, Subtitle files, JSON, Text]

**Output Format:** [WAV voiceover audio, SRT subtitles, JSON line-timing manifest, and optional TXT or JSON transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-line timing and cached line audio support editing and selective regeneration.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
