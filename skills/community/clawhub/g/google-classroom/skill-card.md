## Description:

Helps agents use a connected Google Classroom account to manage courses, coursework, participants, submissions, and announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, administrators, and developers use this skill to help an agent inspect and manage Google Classroom courses, assignments, submissions, participants, and announcements through an authorized connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account may grant Maton access to Google Classroom data.

Mitigation: Review OAuth scopes, authorize only the needed access, and prefer read-only access where possible.

Risk: Writes or deletions can change courses, coursework, and participant records.

Mitigation: Confirm each write or deletion with the user and verify the exact resource IDs first.

Risk: Hosted functions and triggers can keep acting or forwarding data after setup.

Mitigation: Enable them only with explicit approval, review their access and destinations, and remove them when no longer needed.

## Reference(s):

- [Google Classroom skill on ClawHub](https://clawhub.ai/byungkyu/skills/google-classroom)
- [Maton](https://maton.ai)
- [Related API gateway skill](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with shell and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account access depends on the user's authorized connection.]

## Skill Version(s):

1.2.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
