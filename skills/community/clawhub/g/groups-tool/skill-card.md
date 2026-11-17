## Description:

Display user group memberships on the system for permission auditing and access control verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and agents managing Unix-like systems use this skill to inspect local user group memberships for permission auditing and access-control checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local account and group names may be exposed when group membership output is shared.

Mitigation: Use the skill only on authorized systems and avoid sharing raw output outside the operational context that needs the access-control information.

Risk: The included helper may not support every option or username lookup documented by the skill text.

Mitigation: Verify command behavior in the target environment before relying on it for operational audits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/groups-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local system group data only; no network access or external API calls are indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
