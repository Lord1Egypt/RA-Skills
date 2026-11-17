## Description:

Turns talking-head scripts into cloned-voice WAV audio, timed SRT subtitles, and per-line timing manifests through the Miragea API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghhu](https://clawhub.ai/user/yanghhu)

### License/Terms of Use:

MIT

## Use Case:

Content creators and developers use the skill to turn talking-head scripts into voiceover audio, captions, and line timings, and to revise individual lines without re-recording. Use only your own voice or one you are authorized to clone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can imitate someone without their consent.

Mitigation: Use only your own voice or a voice you have explicit authorization to clone; do not imitate public figures or other unauthorized people.

Risk: Reference audio and media sent for voiceover or recognition are processed by Miragea's service.

Mitigation: Avoid sending sensitive media and review Miragea's terms before using the service with personal or client content.

Risk: The security review reports medium confidence, partial analysis, and possible mismatches between advertised and implemented behavior.

Mitigation: Confirm critical commands and outputs with a small sample before relying on them in production; dry-run checks the local workflow but does not validate cloud results.

## Reference(s):

- [Miragea API](https://miragea.ai/v1)
- [Miragea API key setup](https://miragea.ai/workspace/api)
- [ClawHub release](https://clawhub.ai/yanghhu/skills/koubo-voiceover)

## Skill Output:

**Output Type(s):** [Audio files, Subtitles, JSON manifest, Per-line audio files]

**Output Format:** [WAV audio, SRT subtitles, and JSON timing manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-line audio; dry-run creates silent placeholder audio and timing data without calling the API.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
