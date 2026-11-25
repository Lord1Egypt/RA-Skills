## Description:

InternetData (internetdata.io). Use this skill for ANY InternetData request — searching and reading data. Whenever a task involves InternetData, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up an IPv4 or IPv6 address and retrieve its geographic, network, organization, abuse contact, hostname, and Tor or relay details through InternetData.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because it directs users to run a remotely downloaded installer that the scan says is unexplained by the IP lookup purpose.

Mitigation: Before installation, independently verify the installer and understand its system changes.

Risk: IP addresses used for lookup are reported as transmitted through OOMOL to InternetData, and the scan was partial with unresolved references and unknown installer behavior.

Mitigation: Consider whether the address is sensitive and review the installer and unresolved references before using or installing the skill.

## Reference(s):

- [InternetData homepage](https://internetdata.io)
- [InternetData API documentation](https://docs.internetdata.io)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [Structured lookup results with optional text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Address lookup fields may include country, ASN, company, abuse contact, hostname, and Tor, relay, or network flags.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
