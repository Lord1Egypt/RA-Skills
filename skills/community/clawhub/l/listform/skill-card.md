## Description: <br>
List is a smart form and notes skill that records expenses, shipments, logs, reminders, and attachments into local structured JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture everyday bookkeeping, notes, shipment records, operational logs, and attachment archives through natural-language prompts such as "记一下". <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save user-provided records and attachments immediately after clear command-style prompts. <br>
Mitigation: Use it only in workspaces where local record persistence is expected, and confirm ambiguous requests before recording. <br>
Risk: Bookkeeping notes and document attachments may contain personal, financial, or sensitive business information. <br>
Mitigation: Avoid storing secrets or highly sensitive documents unless workspace access, retention, and deletion practices are managed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kobenfang/listform) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kobenfang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown responses with JSON-backed local records and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records and attachments are saved under workspace/memory/list-data when the skill is invoked.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
