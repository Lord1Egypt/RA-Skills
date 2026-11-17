## Description:

Create short brand jingles from a brand name, tone keywords, and campaign context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and brand or marketing teams use this skill to turn a brand name, tone keywords, and intended placement into short audio-logo deliverables. It guides lyric drafting, music-style selection, vocal and instrumental generation, and a spoken brand-name read through SenseAudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand and campaign details are sent to SenseAudio during lyrics, music, and text-to-audio generation.

Mitigation: Use only non-confidential brand or campaign details that the user is willing to share with SenseAudio.

Risk: Shell templates may handle raw user-provided brand text unsafely when building JSON request bodies.

Mitigation: Rewrite request construction to serialize JSON with jq or another safe serializer before running the commands.

Risk: Polling loops can run indefinitely if API tasks do not return a terminal status.

Mitigation: Add bounded polling timeouts and clear failure handling before execution.

Risk: Security evidence marks the release suspicious.

Mitigation: Review the skill before installing or running it, especially the external API calls and shell snippets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/jingle-forge)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline bash code blocks, generated audio URLs, and an MP3 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and the curl, jq, and xxd command-line tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
