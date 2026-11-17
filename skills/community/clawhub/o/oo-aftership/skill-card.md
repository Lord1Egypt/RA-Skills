## Description:

Use an OOMOL-connected AfterShip account to inspect courier and tracking data and manage tracking records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can look up couriers and shipment tracking status, and create, update, complete, retrack, or delete tracking records through their connected AfterShip account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the user to execute an external installer whose release and service implementation were not verified.

Mitigation: Review and install a trusted CLI release, and require separate approval before running the installer.

Risk: The integration uses connected-account access and may automatically synchronize skills.

Mitigation: Review the connected-account access, disable automatic synchronization if unwanted, and keep approval checks for tracking changes and deletion.

## Reference(s):

- [AfterShip Tracking API documentation](https://www.aftership.com/docs/tracking/fcd9acb5f448a-api-overview)
- [AfterShip](https://www.aftership.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON responses with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracking changes require user approval; deletion requires approval of the target.]

## Skill Version(s):

1.0.5 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
