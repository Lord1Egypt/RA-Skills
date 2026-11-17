## Description:

Use a connected Google Ads account to retrieve account data, manage campaigns and ad groups, and work with Customer Match lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and account operators use the skill to inspect Google Ads accounts and manage campaigns, ad groups, and Customer Match lists through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified downloaded code or install additional agent skills.

Mitigation: Review and install a verified CLI release yourself, and check its effects on other agent skills before enabling this skill.

Risk: Actions can change Google Ads campaigns or upload customer-list data through the connected account.

Mitigation: Review each proposed change or upload and confirm its exact target and effect before execution.

## Reference(s):

- [Google Ads](https://ads.google.com)
- [Google Ads API documentation](https://developers.google.com/google-ads/api/docs/start)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands for Google Ads actions and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and write actions use the connected account; confirm proposed changes and Customer Match uploads before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
