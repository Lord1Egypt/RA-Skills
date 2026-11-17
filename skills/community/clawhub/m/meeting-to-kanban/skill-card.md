## Description:

Convert meeting notes or transcripts into a clean Kanban board with owners, due dates, blockers, and next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and project teams use this skill to turn meeting notes or transcripts into an actionable Kanban board with owners, due dates, blockers, and open questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting content and generated CSVs may be untrusted, especially when received from other people.

Mitigation: Review generated board content before sharing it and treat exported files as untrusted inputs.

Risk: CSV cells derived from meeting text could be interpreted by spreadsheet software as formulas.

Mitigation: Sanitize formula-prefixed values before opening exported CSVs in spreadsheet applications.

Risk: The local Python helper reads a user-specified JSON file and writes a CSV file.

Mitigation: Run it only against intended input paths and choose an explicit output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/meeting-to-kanban)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional CSV output from a local Python helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a Kanban CSV, manager summary, owners and due dates table, and open questions list.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
