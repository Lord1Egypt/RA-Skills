## Description:

Search WhoisFreaks for domain availability, domain and IP WHOIS records, ASN records, and subdomain information through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure or security teams can use this skill to check domain availability and retrieve WHOIS records or subdomain listings from a connected WhoisFreaks account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional CLI setup path uses an unverified remote installer, and the executable has not been verified.

Mitigation: Review setup before installing and use a verified CLI release.

Risk: Startup synchronization may change other agents’ installed skills without clear user control.

Mitigation: Approve local changes separately and consider disabling startup skill synchronization before its first run.

Risk: Connecting WhoisFreaks entrusts OOMOL with account access and lookup requests.

Mitigation: Review the connection setup before installing or connecting the skill.

## Reference(s):

- [WhoisFreaks documentation](https://whoisfreaks.com/documentation/)
- [WhoisFreaks](https://whoisfreaks.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-whoisfreaks)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON lookup responses with shell command guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup actions are read-only and require the oo CLI and a connected WhoisFreaks account.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
