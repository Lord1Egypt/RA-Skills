## Description:

Manage Google Classroom courses, coursework, students, teachers, submissions, and announcements via the Google Classroom API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to inspect Google Classroom courses and rosters, review coursework and submissions, and perform confirmed changes such as assignments, announcements, grades, or roster updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external ClawLink plugin and OAuth broker for Google Classroom access.

Mitigation: Install only if ClawLink and the ClawHub plugin package are trusted, and connect the least-privileged Google account that fits the task.

Risk: Grade, roster, coursework, course deletion, and announcement changes can affect real classroom data.

Mitigation: Review previews carefully and require explicit confirmation before any write or destructive operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-classroom-education)
- [Google Classroom API Reference](https://developers.google.com/classroom/reference/rest)
- [Google Classroom API Overview](https://developers.google.com/classroom/api/guides/overview)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-classroom-education)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Google Classroom account through ClawLink; write operations should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
