## Description: <br>
Creates scheduled AI diary entries that reflect on daily interactions, save them as Markdown, and optionally send them to a configured channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyzbcy](https://clawhub.ai/user/lyzbcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to configure a scheduled diary workflow that writes reflective entries, reviews past entries, and optionally sends entries to a selected channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries may summarize prior interactions and include private or sensitive details. <br>
Mitigation: Disable interaction inclusion when privacy matters, or preview entries before saving or sending them. <br>
Risk: Automatic sending can disclose diary content to an unintended channel or recipient. <br>
Mitigation: Set channel and target to trusted destinations and require preview or confirmation before send or write_and_send actions. <br>
Risk: Stored diary files can remain in the workspace for the configured retention period. <br>
Mitigation: Use an appropriate retentionDays value and run cleanup or delete stored diary files when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyzbcy/lyzbcy-diary) <br>
- [Diary template](artifact/templates/default.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown diary entries with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save daily entries under diary/YYYY-MM-DD.md and send them through a configured channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
