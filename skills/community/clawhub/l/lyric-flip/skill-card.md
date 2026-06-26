## Description: <br>
Rewrite song lyrics with a new theme while preserving the original rhyme scheme, line structure, and rhythmic skeleton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to collect reference lyrics and a target theme, extract the original structure, generate constrained replacement lyrics, check rhyme alignment, and optionally submit approved lyrics to SenseAudio for song generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lyric prompts, structure details, approved lyrics, style choices, and song-generation parameters are sent to SenseAudio using the user's API key. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid private or confidential material, and review the generated prompt before API submission. <br>
Risk: Reference or rewritten lyrics may include copyrighted material the user is not allowed to share or transform. <br>
Mitigation: Use only material the user is permitted to provide and review generated lyrics before submitting them for music generation. <br>


## Reference(s): <br>
- [ClawHub Lyric Flip release](https://clawhub.ai/scikkk/lyric-flip) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and a final lyrics, audio, cover, and duration summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY plus curl and jq when using the SenseAudio API workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
