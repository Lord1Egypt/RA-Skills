## Description: <br>
AI会议助手(Meeting Join)免费版 lets an AI voice bot join Google Meet, Microsoft Teams, and Zoom meetings to transcribe speech, answer questions from meeting context, and generate Markdown meeting notes with decisions, action items, and owners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users use this skill to add an AI voice assistant to authorized online meetings for live transcription, contextual Q&A, and post-meeting Markdown notes. It is intended for routine meeting capture and organization, not high-stakes decisions such as medical diagnosis or legal judgments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can join live meetings and capture private conversation content. <br>
Mitigation: Use it only in meetings where the user has authority to add a bot and participant notice or consent requirements are satisfied. <br>
Risk: Transcripts, summaries, callback data, and generated files may expose sensitive meeting information. <br>
Mitigation: Avoid sensitive calls unless storage and sharing behavior is understood, and keep generated files out of shared folders and source control. <br>
Risk: The skill requires API key configuration and may store credentials. <br>
Mitigation: Use environment variables or protected configuration paths, restrict file permissions, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/meeting-join-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and structured meeting-note output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces meeting transcripts, contextual answers, execution status, logs, and Markdown summaries when the meeting workflow succeeds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
