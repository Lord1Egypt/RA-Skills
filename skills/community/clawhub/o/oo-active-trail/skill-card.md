## Description:

Operate ActiveTrail contacts, groups, memberships, and account balances through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing ActiveTrail through an OOMOL-connected account can look up balances, contacts, groups, and memberships, and manage contact or group records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup relies on downloaded CLI installers whose exact behavior has not been verified, and setup may make broader changes to agent instructions.

Mitigation: Review and install the CLI separately before allowing the skill to run; consider disabling startup skill synchronization using the oo CLI command reference.

Risk: The connected OOMOL account mediates access to ActiveTrail contacts, including changes and deletions.

Mitigation: Retain approval for contact or group changes and deletions, and confirm the target and effect before execution.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ActiveTrail API documentation](https://webapi.mymarketing.co.il/api/docs/Guides)
- [ActiveTrail](https://www.activetrail.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses reflect the requested ActiveTrail read or change.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
