## Description: <br>
Reads meeting minutes, summarizes and stores one meeting locally for follow-up Q&A, and uses SenseAudio TTS to generate MP3 audio for the summary and later answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to work with one meeting note, preserve local context for follow-up questions, and create spoken MP3 versions of the summary and answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled local meeting memory may contain stale or sensitive meeting text. <br>
Mitigation: Review or delete memory/current_meeting.json and memory/latest_meeting.json before installing or running the skill. <br>
Risk: Meeting text and generated answers are sent to SenseAudio when creating MP3 output. <br>
Mitigation: Use the skill only for meeting notes that are appropriate to convert through SenseAudio, and set SENSEAUDIO_API_KEY only when that account should be used. <br>


## Reference(s): <br>
- [Product brief](PRD.md) <br>
- [SenseAudio API key documentation](https://senseaudio.cn/docs/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON command results, and local MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores meeting context in local JSON memory and writes generated audio to user-specified MP3 paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
