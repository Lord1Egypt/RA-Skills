## Description: <br>
全流程会议助理虾 transcribes meeting recordings, creates meeting notes, extracts action items, and distributes confirmed tasks through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to process meeting audio into local transcripts, concise meeting summaries, and actionable task lists. With user confirmation, it can distribute identified tasks to responsible people through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings and full transcripts may contain sensitive business or personal information. <br>
Mitigation: Process recordings locally, store transcript outputs in a controlled ./transcripts/ location, and avoid using the skill for meetings that should not be shared through Feishu. <br>
Risk: The Feishu app credentials can access contacts and send bot messages. <br>
Mitigation: Use a dedicated least-privilege Feishu app, protect FEISHU_APP_SECRET, and keep only the permissions needed for contact lookup and message delivery. <br>
Risk: Incorrectly extracted tasks or recipients could send misleading action items to the wrong person. <br>
Mitigation: Preview recipients and message bodies, require explicit user confirmation before sending, and skip unresolved recipients while reporting them back to the user. <br>


## Reference(s): <br>
- [Feishu Message API quick reference](references/feishu-message-api.md) <br>
- [ClawHub release page](https://clawhub.ai/tujinsama/meeting-assistant-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, local transcript files, and Feishu message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before sending Feishu messages; saves full transcripts under ./transcripts/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
