## Description:

Search DiscoLike and retrieve company profiles, certificate metrics, digital footprint scores, growth metrics, and account usage through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover companies and retrieve DiscoLike firmographic and digital presence data, using the user's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software without a separate approval step.

Mitigation: Install a reviewed oo CLI release yourself and check whether its automatic skill synchronization is wanted before enabling the skill.

Risk: OOMOL will broker access to the user's connected DiscoLike account.

Mitigation: Review the setup and connected account before use, and only connect an account appropriate for the requested lookups.

## Reference(s):

- [DiscoLike API documentation](https://docs.discolike.com/)
- [DiscoLike](https://discolike.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [Structured JSON results and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected DiscoLike account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
