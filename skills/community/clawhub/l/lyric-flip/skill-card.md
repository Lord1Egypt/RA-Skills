## Description:

Lyric Flip helps agents rewrite songs around new themes while preserving rhyme scheme, line structure, rhythmic skeleton, and singability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to transform reference lyrics into themed parody or replacement lyrics with controlled structure and rhyme. The agent can guide skeleton extraction, lyric generation, rhyme checking, and optional SenseAudio music creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lyric prompts, approved lyrics, and style information are sent to SenseAudio.

Mitigation: Use only content you are comfortable sharing with SenseAudio, avoid sensitive or private lyrics, and review usage costs before running API calls.

Risk: The artifact includes shell examples that interpolate user-controlled lyric and prompt text into JSON payloads.

Mitigation: Build JSON payloads with a proper JSON encoder and review commands before execution.

Risk: The workflow may proceed from lyric generation to full music generation.

Mitigation: Ask for explicit user confirmation before submitting approved lyrics for music creation.

## Reference(s):

- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/lyric-flip)
- [ClawHub Publisher Profile](https://clawhub.ai/user/scikkk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with structured lyric text, command examples, and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY plus curl and jq for SenseAudio API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
