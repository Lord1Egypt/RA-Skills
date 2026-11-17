## Description:

Chargeblast (chargeblast.com). Use this skill for ANY Chargeblast request — reading, creating, and updating data. Whenever a task involves Chargeblast, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External Chargeblast account users can retrieve alerts, orders, merchants, and deflection logs, and can create credit requests or update alerts through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code or make broad agent changes without clear approval.

Mitigation: Install a verified oo CLI release, review and approve local changes, and review or disable automatic agent-skill synchronization.

Risk: Connecting Chargeblast grants OOMOL access to the connected account.

Mitigation: Limit account permissions and require confirmation for credit requests and alert updates.

## Reference(s):

- [Chargeblast API documentation](https://docs.chargeblast.com/)
- [Chargeblast](https://www.chargeblast.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text]

**Output Format:** [JSON action results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require user confirmation before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
