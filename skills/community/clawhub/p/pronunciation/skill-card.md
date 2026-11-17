## Description:

Foreign language pronunciation coach that generates standard TTS, compares a user's recording against the practice text, gives word-level feedback, and creates targeted pronunciation drills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to practice foreign-language pronunciation, compare recordings against target text, and receive word-level feedback with targeted drills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Practice text and voice recordings are sent to the external SenseAudio API.

Mitigation: Install only when users understand the external processing path and collect recordings only with clear user opt-in.

Risk: Documented shell commands can run unintended commands or upload the wrong local file if user-provided values are not constrained.

Mitigation: Use a constrained runner that serializes JSON safely, passes curl arguments without a shell, and validates recording paths and language codes.

Risk: Progress tracking can store pronunciation history and error patterns in a local file.

Mitigation: Store progress only after opt-in and keep it in a private app-state location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scikkk/skills/pronunciation)
- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)
- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2)
- [SenseAudio transcription API endpoint](https://api.senseaudio.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3 pronunciation examples, JSON API responses, ASR transcript files, and a pronunciation_progress.json progress file when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
