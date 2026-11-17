## Description:

Operate Planhat through an OOMOL-connected account to read, create, and update company and end-user records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer success teams use the skill to read Planhat company and end-user records and to create or update them through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute remote CLI installers whose local effects could not be inspected.

Mitigation: Review CLI installation separately, use a pinned and verified release, and check whether it installs or updates other agent skills.

Risk: Create and update actions change Planhat records.

Mitigation: Confirm the exact payload and effect with the user before write actions; get explicit approval before any destructive action.

## Reference(s):

- [Planhat](https://www.planhat.com)
- [Planhat API documentation](https://docs.planhat.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Planhat ClawHub release](https://clawhub.ai/oomol/skills/oo-planhat)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and Planhat data responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve records; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
