## Description: <br>
Guides agents through SenseAudio music APIs to generate lyrics, create songs with style and vocal controls, and poll asynchronous tasks for results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call SenseAudio's external service for AI-generated lyrics and full songs, including asynchronous polling for completed audio results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SenseAudio's external service and requires an API key. <br>
Mitigation: Use a dedicated, revocable SENSEAUDIO_API_KEY and avoid hardcoding real keys in shared files. <br>
Risk: Prompts, lyrics, and song generation requests may contain confidential, regulated, personal, or proprietary content. <br>
Mitigation: Submit only content that is appropriate for SenseAudio's data handling terms and the user's organization policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/music-gen) <br>
- [SenseAudio lyrics creation documentation](https://senseaudio.cn/docs/song/lyrics_create) <br>
- [SenseAudio lyrics polling documentation](https://senseaudio.cn/docs/song/lyrics_pending) <br>
- [SenseAudio music creation documentation](https://senseaudio.cn/docs/song/music_create) <br>
- [SenseAudio music polling documentation](https://senseaudio.cn/docs/song/music_pending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with REST examples, JSON response shapes, shell commands, and Python sample code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and sends prompts, lyrics, and generation requests to SenseAudio.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
