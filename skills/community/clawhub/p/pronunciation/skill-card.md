## Description: <br>
Foreign language pronunciation coach that helps users listen to standard TTS pronunciation, record themselves, receive word-by-word feedback, and practice targeted drills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External language learners and agents assisting them use this skill to generate pronunciation examples, compare uploaded speech against practice text, identify likely pronunciation issues, and propose targeted drills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Practice text and voice recordings are sent to SenseAudio for TTS and transcription. <br>
Mitigation: Use non-sensitive phrases and install only when the user accepts sending audio and text to SenseAudio. <br>
Risk: The skill stores detailed local progress in pronunciation_progress.json. <br>
Mitigation: Run the skill in a private working folder and delete pronunciation_progress.json when it is no longer needed. <br>
Risk: Shell examples can mishandle user-supplied practice text if pasted directly into command strings. <br>
Mitigation: Build request JSON safely and avoid interpolating raw user text into shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/pronunciation) <br>
- [Publisher profile](https://clawhub.ai/user/scikkk) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and pronunciation feedback text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local audio artifacts and pronunciation_progress.json during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
