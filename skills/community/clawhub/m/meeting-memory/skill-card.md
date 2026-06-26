## Description: <br>
Record, transcribe, and store meeting notes with persistent semantic memory using BlueColumn for later recall of action items, decisions, and topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and agents use this skill to store meeting audio, transcripts, notes, action items, decisions, and topics in BlueColumn, then recall them later with natural-language questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings, transcripts, notes, and action items may contain confidential, regulated, or third-party content that is sent to BlueColumn for persistent searchable storage. <br>
Mitigation: Confirm meeting consent and review BlueColumn privacy, retention, and deletion requirements before storing sensitive meeting content. <br>
Risk: The skill requires a BlueColumn API key. <br>
Mitigation: Use a revocable API key, keep it private, and avoid logging or exposing it in prompts, command history, or shared output. <br>
Risk: AI-extracted summaries and action items may be incomplete or inaccurate. <br>
Mitigation: Review extracted summaries, action items, and recall answers before relying on them for follow-up work. <br>


## Reference(s): <br>
- [BlueColumn API Reference](references/api.md) <br>
- [BlueColumn](https://bluecolumn.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return meeting summaries, action items, key topics, recall answers, and source references from BlueColumn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
