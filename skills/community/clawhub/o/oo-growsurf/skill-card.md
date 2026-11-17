## Description:

Use the connected GrowSurf account to read and manage campaigns, participants, and referrals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect GrowSurf teams and campaigns and manage participant and referral records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup directs execution of remote installers without a separate approval step; installer contents and hosted connector implementations could not be verified.

Mitigation: Review and approve CLI installation separately using a verified, pinned release. Check its automatic skill-install behavior and connect only the intended GrowSurf account.

Risk: GrowSurf write and deletion actions can change or remove participant and referral data.

Mitigation: Retain the required approvals for writes and deletions, and confirm the exact action and target before execution.

## Reference(s):

- [GrowSurf API documentation](https://docs.growsurf.com/developer-tools/rest-api)
- [GrowSurf homepage](https://growsurf.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [GrowSurf ClawHub page](https://clawhub.ai/oomol/skills/oo-growsurf)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured GrowSurf data and action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected GrowSurf account and the selected action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
