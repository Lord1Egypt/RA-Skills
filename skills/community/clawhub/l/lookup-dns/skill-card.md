## Description:

DNS record lookups, reverse DNS, WHOIS via RDAP, and IP geolocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query DNS records, reverse DNS, RDAP domain information, and IP geolocation through the dns.agentutil.net service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain names and IP addresses submitted for lookup are sent to dns.agentutil.net.

Mitigation: Avoid querying sensitive internal hostnames, private infrastructure, or other data whose disclosure to the external service is not acceptable.

Risk: Returned DNS, RDAP, WHOIS, or geolocation data may be incomplete, stale, or unsuitable as the sole basis for security decisions.

Mitigation: Verify consequential findings with authoritative DNS, registrar, network, or security sources before acting on them.

## Reference(s):

- [DNS Lookup service homepage](https://dns.agentutil.net)
- [ClawHub skill listing](https://clawhub.ai/cutthemustard/skills/lookup-dns)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send queried domains and IP addresses to dns.agentutil.net; free tier allows 10 queries per day.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
