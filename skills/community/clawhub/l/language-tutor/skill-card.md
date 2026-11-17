## Description:

Create language learning audio with SenseAudio TTS, including pronunciation drills, bilingual lessons, slowed speech practice, and dialogue exercises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to generate pronunciation drills, bilingual lessons, slowed listening practice, dialogue exercises, audio clips, and companion study notes through SenseAudio TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lesson text is sent to SenseAudio's external TTS API.

Mitigation: Use only content appropriate for SenseAudio processing and disclose this provider data flow to users.

Risk: The helper process requires access to SENSEAUDIO_API_KEY.

Mitigation: Run the skill in a limited environment, keep the key in the environment only, and avoid logging or saving credentials.

Risk: Runtime behavior depends on local Python packages and optional audio tooling such as ffmpeg.

Mitigation: Pin or review requests and pydub versions before use, and fall back to separate audio files when merge tooling is unavailable.

## Reference(s):

- [Language Tutor on ClawHub](https://clawhub.ai/scikkk/skills/language-tutor)
- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)
- [SenseAudio TTS endpoint](https://api.senseaudio.cn/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python examples, configuration notes, and manifests for generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce individual MP3 clips, merged lesson audio when local audio tooling is available, and companion study notes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
