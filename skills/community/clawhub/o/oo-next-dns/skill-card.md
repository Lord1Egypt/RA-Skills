## Description:

Use an OOMOL-connected NextDNS account to retrieve profiles, DNS logs, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with a connected NextDNS account can retrieve profile settings, DNS query logs, and analytics for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and automatically synchronize skills, which can make broader changes to the agent's skill set.

Mitigation: Review and explicitly authorize setup, prefer a verified fixed release, and disable automatic skill synchronization.

Risk: The connected account can expose sensitive DNS information through logs and analytics.

Mitigation: Connect only the intended NextDNS account and understand the access OOMOL mediates.

## Reference(s):

- [NextDNS](https://nextdns.io/)
- [NextDNS API documentation](https://nextdns.github.io/api/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured connector data with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only profile, DNS log, and analytics results]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
