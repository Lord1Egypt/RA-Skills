## Description:

Read and change your children's school dismissal plans on PickUp Patrol (app.pickuppatrol.net) from a shell with curl — students, weekly defaults, day-by-day changes, school cutoff times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill to review weekly and date-specific school dismissal plans and make plan changes through PickUp Patrol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login credentials may be exposed through shell command arguments or retained exported variables.

Mitigation: Read the password without echoing it, keep it out of command arguments, and avoid retaining exported credentials.

Risk: Authentication output and child records may remain in inadequately protected temporary files.

Mitigation: Use private temporary files and remove them after use.

Risk: A dismissal change may affect how a child leaves school or may not be saved as intended.

Mitigation: Authorize the exact child, dates, and changes, then read the plan back and verify the saved result. Keep health-audit and password operations outside routine dismissal tasks.

## Reference(s):

- [PickUp Patrol API reference](references/api.md)
- [PickUp Patrol API endpoint](https://app.pickuppatrol.net/api/json/reply)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/pickuppatrol-mcp)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline curl, bash, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read and change student dismissal records; changes should be authorized and verified by reading the saved plan.]

## Skill Version(s):

1.3.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
