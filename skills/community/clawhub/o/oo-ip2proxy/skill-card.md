## Description:

IP2Proxy (ip2location.com). Use this skill for ANY IP2Proxy request — searching and reading data. Whenever a task involves IP2Proxy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to check whether a single IPv4 or IPv6 address is associated with a proxy and read the IP2Proxy lookup result through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs installation scripts whose payloads and live connector implementation were not verified, and installation may add other agent skills.

Mitigation: Prefer an existing CLI installation; before setup, review and approve a verified installer and check whether it installs other skills.

Risk: IP addresses submitted for lookup are shared with OOMOL and IP2Proxy.

Mitigation: Submit only IP addresses that may be shared with both services.

## Reference(s):

- [IP2Proxy web service and API documentation](https://www.ip2location.com/web-service/ip2proxy)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [IP2Proxy lookup result with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One IPv4 or IPv6 address per lookup.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
