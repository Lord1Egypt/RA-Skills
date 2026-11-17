## Description:

Operate Altiria through a connected OOMOL account to read and manage contacts and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Altiria account users use this skill to retrieve contact and SMS information, manage contacts, and send SMS through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may run remote CLI installers or install other agent skills without separate approval.

Mitigation: Review and approve CLI installation separately, verify the installer or release, and decide whether automatic installation of other skills is acceptable.

Risk: Connected Altiria access can expose account data, send SMS, or change contacts.

Mitigation: Confirm SMS recipients and content, and confirm contact changes before executing write or destructive actions.

## Reference(s):

- [Altiria API documentation](https://apidocs.altiria.com/)
- [Altiria](https://www.altiria.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON action payloads and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the requested Altiria action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
