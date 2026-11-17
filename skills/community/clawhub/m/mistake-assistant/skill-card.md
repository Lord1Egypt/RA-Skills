## Description:

错题小助手 helps students record mistakes, organize them by subject and topic, schedule spaced review, analyze weak areas, and export mistake books for study.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Students and learning-support agents use this skill to maintain a local mistake log, identify weak subjects or topics, schedule review, and export study materials. It is intended for educational study tracking rather than system administration or external service automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports can be written outside the default export folder when an arbitrary output path is supplied.

Mitigation: Run the skill in a constrained workspace and keep exports inside an approved local directory.

Risk: HTML exports may preserve unsafe user-provided content from mistake records.

Mitigation: Do not open or share HTML exports made from untrusted content; prefer Markdown or JSON for review and backup.

Risk: Mistake records and reports may contain private educational data.

Mitigation: Treat mistake-data and exported reports as private files and avoid syncing or sharing them without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/mistake-assistant)
- [Ebbinghaus forgetting curve review algorithm](references/forgetting_curve.md)
- [Subject and topic taxonomy](references/subjects.json)
- [Mistake entry templates](references/templates.md)
- [Export template](assets/templates/export_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Plain text guidance and local Markdown, JSON, or HTML study artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores mistake records under mistake-data and exports study materials under mistake-exports unless a caller supplies another path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
