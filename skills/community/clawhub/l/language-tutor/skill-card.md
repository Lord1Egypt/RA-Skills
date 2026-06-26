## Description: <br>
Create language learning audio with SenseAudio TTS, including pronunciation drills, bilingual lessons, slowed speech practice, and dialogue exercises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate language-learning audio, pronunciation drills, bilingual lessons, slowed listening practice, dialogue exercises, and companion study notes through SenseAudio TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SenseAudio API key and can call external TTS endpoints. <br>
Mitigation: Read credentials only from SENSEAUDIO_API_KEY, send them only in the Authorization header, and avoid logging or saving secrets. <br>
Risk: Generated lesson files and manifests can expose sensitive learner text or troubleshooting identifiers. <br>
Mitigation: Use deterministic local filenames, review transcripts before sharing, and include trace IDs only when needed for troubleshooting. <br>
Risk: Audio composition may fail or produce incorrect output when local audio dependencies are missing. <br>
Mitigation: Use pydub and an audio backend only when available; otherwise emit individual audio clips and a Markdown manifest. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scikkk/language-tutor) <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, audio files, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, JSON API payloads, file manifests, and generated audio file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and python3; optional local audio merging depends on pydub and an audio backend such as ffmpeg.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
