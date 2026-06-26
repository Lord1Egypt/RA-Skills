## Description: <br>
Converts meeting notes, chat logs, voice transcripts, and bullet notes into structured project status with action items, owners, deadlines, decisions, risks, and milestones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seulkilu](https://clawhub.ai/user/seulkilu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, project managers, and developers use this skill to turn unstructured meeting or chat text into actionable project follow-up records. It is suited for extracting owners, tasks, deadlines, priority, decisions, risks, and next milestones from Chinese, English, or mixed-language notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated action items may assign incorrect owners, deadlines, priorities, or risks when the source notes are ambiguous. <br>
Mitigation: Review generated owners, deadlines, priorities, and risks before treating them as commitments. <br>
Risk: A request for a general summary may still produce project-style action items. <br>
Mitigation: Confirm that the requested output should be action-item oriented before using it for follow-up tracking. <br>


## Reference(s): <br>
- [Entity Recognition & Output Patterns](references/patterns.md) <br>
- [Meeting to Action Items on ClawHub](https://clawhub.ai/seulkilu/meeting-to-action-items) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [Structured Markdown-style text with optional JSON from the bundled parser script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs meeting summary, action items, decisions, risks, and milestones; generated owners, deadlines, priorities, and risks should be reviewed before being treated as commitments.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
