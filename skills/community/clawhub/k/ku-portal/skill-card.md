## Description:

KU Portal lets OpenClaw query Korea University KUPID, library, dining menu, timetable, course, scholarship, notice, and Canvas LMS information through a Python CLI wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Korea University users and OpenClaw agents use this skill to retrieve public campus information and authenticated KUPID or Canvas LMS data such as notices, schedules, scholarships, timetables, courses, assignments, and grades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read KUPID credentials from a local plaintext JSON file.

Mitigation: Keep the credential file and parent directory private, use restrictive permissions such as chmod 600, avoid shared machines, and rotate the password if it is exposed.

Risk: The setup script installs or upgrades ku-portal-mcp without a pinned package version, and that package receives the configured credentials for login features.

Mitigation: Review or pin the ku-portal-mcp package before running setup, and install it inside the skill virtual environment.

Risk: Authenticated commands may retrieve personal academic, course, assignment, grade, and session data.

Mitigation: Run the skill only in trusted local environments and protect or clear session cache and log files on shared or managed systems.

## Reference(s):

- [KU Portal ClawHub listing](https://clawhub.ai/garibong-labs/skills/ku-portal)
- [Publisher profile](https://clawhub.ai/user/garibong-labs)
- [ku-portal-mcp upstream project](https://github.com/SonAIengine/ku-portal-mcp)
- [garibong-labs ku-portal-mcp fork](https://github.com/garibong-labs/ku-portal-mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text CLI output, Markdown command examples, JSON credential configuration, and optional ICS calendar file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require a local KUPID credential file and may use session caches; timetable export writes an ICS file to the user's Downloads directory.]

## Skill Version(s):

0.3.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
