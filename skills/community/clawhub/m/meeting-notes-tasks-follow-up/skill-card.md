## Description:

Lightweight meeting-notes productivity workflow for turning transcripts or raw meeting notes into clean summaries, extracted key points, and simple action lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaelbuenobarthe](https://clawhub.ai/user/gaelbuenobarthe)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and collaborators use this skill to convert raw meeting transcripts, call notes, workshop notes, or internal sync notes into a concise recap with key points, explicit tasks, owners when stated, and open questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV task exports from untrusted meeting notes may be unsafe to open directly in spreadsheet software if formula-leading cells are present.

Mitigation: Sanitize formula-leading cells before opening generated CSV files from untrusted transcripts, and review extracted tasks because the extraction logic is heuristic.

## Reference(s):

- [Templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/gaelbuenobarthe/skills/meeting-notes-tasks-follow-up)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown recap and task list, with optional JSON summary and CSV task files from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task extraction is heuristic; unknown owners are left unassigned and missing due dates are not guessed.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
