## Description:

Manage MemberVault users and course access through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

MemberVault account owners and operators use this skill to list courses, add users, manage product access, and delete user records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded code without separate approval or integrity verification, and the remote installers and hosted backend were not verified.

Mitigation: Install a reviewed CLI yourself, require approval before downloaded code runs, and decide whether to disable automatic skill synchronization.

Risk: Adding users, removing access, or deleting users can change or erase MemberVault account data.

Mitigation: Keep the skill's confirmation requirements and verify the exact target and effect before each write or destructive action.

Risk: The skill handles MemberVault credentials and operation data through the connected OOMOL account.

Mitigation: Use a reviewed connection and limit account access to the intended MemberVault operations.

## Reference(s):

- [MemberVault](https://membervault.co/)
- [MemberVault API documentation](https://intercom.help/membervault/en/articles/6869595-api-endpoints-advanced)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [MemberVault skill listing](https://clawhub.ai/oomol/skills/oo-membervault)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [JSON requests, CLI commands, and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live action schema to shape requests; writes and deletions require confirmation.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
