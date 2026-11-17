## Description: <br>
HeyGen TTS免费版 guides agents through HeyGen Starfish text-to-speech workflows for voice lookup, multilingual speech generation, speed control, and audio download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual creators and developers use this skill to generate multilingual speech with HeyGen's cloud TTS API for video narration, audiobooks, and localized content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to HeyGen's cloud service for speech generation. <br>
Mitigation: Use it only when third-party TTS processing is approved, and avoid submitting confidential, regulated, or sensitive text unless that processing is allowed. <br>
Risk: The workflow requires a HeyGen API key. <br>
Mitigation: Treat HEYGEN_API_KEY as a secret, store it outside prompts and source files, and avoid hard-coding it in examples or generated scripts. <br>
Risk: Downloaded audio files could overwrite existing local files if an unsafe output path is chosen. <br>
Mitigation: Use explicit, reviewed output paths and check before writing or replacing generated audio files. <br>
Risk: Broad activation language may cause the skill to be used for unrelated translation, data, or automation tasks. <br>
Mitigation: Use this skill for HeyGen speech generation workflows and choose a more specific tool for unrelated translation or general automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/heygen-tts-tool-free) <br>
- [HeyGen voice list API](https://api.heygen.com/v3/voices?engine=starfish&language=Chinese) <br>
- [HeyGen speech generation API](https://api.heygen.com/v3/voices/speech) <br>
- [HeyGen API base URL](https://api.heygen.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, Python snippets, configuration steps, and structured response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HEYGEN_API_KEY secret and may produce or download WAV audio from a HeyGen audio_url.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
