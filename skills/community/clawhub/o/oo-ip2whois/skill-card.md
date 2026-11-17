## Description:

Looks up domain WHOIS registration details and lists domains hosted on an IP address through an IP2WHOIS connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up domain registration information or discover domains hosted on an IP address through their connected IP2WHOIS service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup behavior may execute remote installers that have not been verified.

Mitigation: Review setup behavior before installation and prefer installing a reviewed CLI version yourself. Require approval for dependency installation.

Risk: Automatic skill synchronization may make broader changes to agent skills.

Mitigation: Review or disable automatic skill synchronization using the publisher's documented controls.

Risk: Lookup requests use connected credentials through OOMOL and may incur charges.

Mitigation: Review the connected account and monitor usage and billing before running lookups.

## Reference(s):

- [IP2WHOIS API documentation](https://www.ip2whois.com/developers-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [OOMOL IP2WHOIS connection setup](https://console.oomol.com/connections/ip2whois)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured lookup data with concise textual results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields depend on the requested domain or IP and the provider response.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
