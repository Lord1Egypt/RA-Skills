## Description: <br>
智能会议机器人免费版 helps an agent join meetings, monitor speaker state, and transcribe meeting audio for basic meeting records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent join permitted meetings, monitor voice state, produce timestamped transcripts, and save records for personal meeting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can join live meetings and transcribe speech without sufficient consent guidance. <br>
Mitigation: Use it only for meetings where participants have agreed to the bot joining and to transcription. <br>
Risk: Meeting platform APIs or transcription services may receive meeting data. <br>
Mitigation: Confirm which meeting platform and transcription service are used before sharing sensitive meeting content. <br>
Risk: Saved transcripts may contain sensitive personal or business information. <br>
Mitigation: Clarify where transcript files are written and define retention, deletion, and disablement practices before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/join-meeting-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include meeting transcript text with speaker labels, timestamps, execution logs, and local-file save guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
