## Description:

Predict ranked country candidates and probabilities for names using Nationalize (nationalize.io).

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request nationality predictions for a single name or a batch of names, then read ranked country candidates and probabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run unverified remote code, and synchronization may change installed agent skills more broadly than expected.

Mitigation: Review setup, provision a verified oo CLI release, and set OO_SKILLS_SYNC_DISABLED if you do not want automatic skill synchronization. Submit only names you are authorized to share with OOMOL and Nationalize.

## Reference(s):

- [Nationalize](https://nationalize.io/)
- [Nationalize API reference](https://nationalize.io/documentation/api/reference)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON responses with ranked country candidates and probabilities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch predictions accept up to 100 names; each name uses one lookup.]

## Skill Version(s):

1.0.2 (source: frontmatter metadata, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
