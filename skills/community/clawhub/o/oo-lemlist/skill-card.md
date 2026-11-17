## Description:

Use lemlist through a connected OOMOL account to search and read campaign, lead, and team data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected lemlist account can retrieve campaign details, campaign leads, and team information through the skill's read actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes unpinned remote installers without an explicit approval step; the installers and hosted implementation were not audited.

Mitigation: Review the CLI installation and use a pinned, verified release where possible. Check which additional skills it installs and review the lemlist permissions granted through OOMOL.

## Reference(s):

- [lemlist](https://www.lemlist.com)
- [lemlist API documentation](https://developer.lemlist.com/api-reference/getting-started/overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results for campaigns, campaign leads, and team information; response fields vary by action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
