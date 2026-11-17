## Description:

Creates first-person pet narration videos by analyzing pet body language, writing personality-matched narration, generating speech audio, and merging the audio with the source video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanglinghao01-rakuten](https://clawhub.ai/user/zhanglinghao01-rakuten)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn pet videos into humorous first-person narration videos. The agent analyzes visible pet behavior, drafts narration aligned to action timing, generates speech audio, and prepares final media files for review or editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet videos and narration text may be sent to video-understanding or text-to-speech tools selected by the agent.

Mitigation: Confirm the target tools and data-sharing posture before use, especially when videos contain private homes, people, locations, or other sensitive context.

Risk: The skill is primarily written for Mandarin narration, so voice and language choices may not match user expectations by default.

Mitigation: Confirm narration language, voice, and tone before generating speech audio.

Risk: Local video merging may require ffmpeg installation in the agent environment.

Mitigation: Install or allow ffmpeg only in trusted environments where local media processing is expected.

## Reference(s):

- [Pet Body Language Reference Manual](references/pet-body-language.md)
- [ClawHub skill page](https://clawhub.ai/zhanglinghao01-rakuten/skills/pet-video-narration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with narration text, timing notes, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an MP4 video, merged audio file, and segmented audio files when the agent has suitable video, speech, and ffmpeg tooling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
