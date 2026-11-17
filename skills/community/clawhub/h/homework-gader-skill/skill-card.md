## Description:

Downloads homework ZIP attachments from QQ email, grades programming submissions against templates with AI assistance, and writes an Excel grade report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaouuu](https://clawhub.ai/user/yaouuu)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers who collect programming homework through QQ email can use this skill to download unread ZIP attachments, match submissions to an assignment, request AI-assisted grading against a template, and produce a spreadsheet of scores and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles QQ email credentials and mailbox content.

Mitigation: Use only a dedicated QQ mailbox with an app-specific authorization code, and avoid running the skill where unrelated host credentials or sensitive files are accessible.

Risk: The skill processes untrusted ZIP attachments and student submissions.

Mitigation: Process mail only from trusted senders, run in an isolated workspace, and fix ZIP download and extraction handling before production use.

Risk: Student submissions can influence AI-assisted grading and generated comments.

Mitigation: Review generated scores and feedback before relying on or sharing the grades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaouuu/skills/homework-gader-skill)
- [Publisher profile](https://clawhub.ai/user/yaouuu)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [JSON object containing an Excel file path; generated report is an .xlsx file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report contains student names, student IDs, assignment numbers, scores, and brief grading comments when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
