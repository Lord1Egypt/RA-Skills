## Description:

Use TalentHR through an OOMOL-connected account to change an employee's user role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HR staff and administrators use this skill to change an employee's TalentHR role through their connected account. Confirm the employee and intended role before making the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes downloaded CLI installation commands, and the installer and hosted connector were not verified.

Mitigation: Review and install the CLI separately; avoid the automatic download-and-execute fallback. Check whether OO_SKILLS_SYNC_DISABLED is appropriate using the oo CLI command reference.

Risk: Changing an employee role can alter account access.

Mitigation: Confirm the employee and intended role with the user before every change.

## Reference(s):

- [TalentHR API documentation](https://apidocs.talenthr.io/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [TalentHR homepage](https://www.talenthr.io/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON connector responses and shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role changes require confirmation of the employee and intended role before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
