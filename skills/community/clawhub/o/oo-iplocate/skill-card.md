## Description:

IPLocate (iplocate.io). Use this skill for ANY IPLocate request — searching and reading data. Whenever a task involves IPLocate, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up geolocation, ASN, privacy, hosting, company, and abuse information for one or more IP addresses, or to inspect the connector server's outgoing IP address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and install additional persistent agent skills.

Mitigation: Review and verify the CLI installation source before setup, and consider disabling automatic skill synchronization.

Risk: Submitted IP addresses pass through OOMOL to IPLocate.

Mitigation: Submit only IP addresses you are authorized to share.

## Reference(s):

- [IPLocate homepage](https://www.iplocate.io/)
- [IPLocate API documentation](https://www.iplocate.io/docs/ip-intelligence-api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-iplocate)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON response containing IP geolocation and intelligence data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include lookup data for one or more IP addresses, with per-IP errors for batch lookups.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
