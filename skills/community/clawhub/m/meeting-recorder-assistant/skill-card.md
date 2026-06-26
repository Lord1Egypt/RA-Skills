## Description: <br>
Intelligent meeting recording and transcription assistant with automated minutes generation, action item extraction, and sentiment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to record meetings, transcribe audio, generate structured meeting minutes, extract action items, and analyze meeting content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture sensitive meeting audio and create transcript or minutes files. <br>
Mitigation: Use it only with participant consent, avoid regulated or confidential meetings unless policy permits, and deliberately manage retention and deletion of audio and transcript files. <br>
Risk: Transcription can send meeting audio data to Google's speech recognition service. <br>
Mitigation: Use Google-based transcription only where policy allows it; for sensitive deployments, consider replacing it with an approved local-only transcription option. <br>
Risk: Runtime dependencies affect how audio is captured and processed. <br>
Mitigation: Pin and review dependencies before deployment, especially in environments that process sensitive meeting data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/meeting-recorder-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/kaiyuelv) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python usage examples, JSON transcript and minutes data, Markdown meeting minutes, and TXT transcript text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audio, transcript, JSON, Markdown, and TXT files depending on how the agent uses the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
