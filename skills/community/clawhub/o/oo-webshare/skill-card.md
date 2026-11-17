## Description:

Webshare (webshare.io). Use this skill for ANY Webshare request — searching and reading data. Whenever a task involves Webshare, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Webshare through an OOMOL-connected account can use this skill to read account profiles, proxy configuration and listings, and hourly usage statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run remote installers that were not verified.

Mitigation: Review and install a trusted oo CLI version yourself before using the skill.

Risk: Setup does not disclose broader changes to installed agent skills, and returned account or proxy information is sensitive.

Mitigation: Review publisher-documented controls and consider disabling automatic skill synchronization; connect only the intended Webshare account and treat returned data as sensitive.

## Reference(s):

- [Webshare API documentation](https://apidocs.webshare.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Webshare homepage](https://www.webshare.io/)

## Skill Output:

**Output Type(s):** [JSON data, Account and proxy information]

**Output Format:** [JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only profile, proxy configuration, proxy listing, and usage-statistics data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
