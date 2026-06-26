## Description: <br>
Convert meeting notes or transcripts into a clean Kanban board with owners, due dates, blockers, and next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, project managers, and team leads use this skill to turn meeting notes or transcripts into action-oriented Kanban outputs, including owners, due dates, blockers, and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes may omit owners, due dates, or context needed for a reliable board. <br>
Mitigation: Mark missing fields as unresolved and ask only for the minimum clarification needed. <br>
Risk: Generated task boards may be mistaken for final commitments or official records. <br>
Mitigation: Return a preview or draft first and keep assumptions explicit before downstream use. <br>
Risk: The helper script writes a CSV output path supplied by the user. <br>
Mitigation: Use explicit input and output paths and avoid overwriting existing files without confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/meeting-to-kanban) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CSV-style task tables and optional local CSV file generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit meeting input and optional board-column schema; missing owners, dates, or facts should be marked unresolved.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
