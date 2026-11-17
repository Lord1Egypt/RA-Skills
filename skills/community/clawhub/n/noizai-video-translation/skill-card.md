## Description:

Translate and dub videos from one language to another, replacing the original audio with TTS while keeping the video intact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksuriuri](https://clawhub.ai/user/ksuriuri)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to translate a video's spoken content into a target language, generate dubbed TTS audio, and merge it back into the original video. It is intended for videos with available subtitles and media that the user is allowed to process with the referenced services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on unpinned third-party downloader and TTS skills.

Mitigation: Review and pin those dependencies before installation, then run the workflow in a restricted working directory.

Risk: Source video and reference audio may be processed by the referenced cloud TTS backend.

Mitigation: Use only media whose voice and content may be sent to that backend, and prefer minimal reference audio clips when practical.

Risk: The skill may store NOIZ_API_KEY in plaintext project configuration if the user chooses persistence.

Mitigation: Prefer environment-level secret storage and avoid committing .env files or API-key configuration to source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksuriuri/skills/noizai-video-translation)
- [youtube-downloader skill](https://github.com/crazynomad/skills/blob/master/youtube-downloader/SKILL.md)
- [NoizAI tts skill](https://github.com/NoizAI/skills/blob/main/skills/tts/SKILL.md)
- [Noiz API keys](https://developers.noiz.ai/api-keys)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow produces a final dubbed video file path on success and a clear download, TTS, or audio replacement error on failure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
