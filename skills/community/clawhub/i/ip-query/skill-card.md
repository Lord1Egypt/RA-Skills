## Description:

ip-query helps an agent query the current device's public IP address and optionally report approximate location, ISP, and organization details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shogunwin](https://clawhub.ai/user/shogunwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to answer public-IP questions, verify outbound network identity, and optionally inspect coarse geolocation and ISP metadata returned by public lookup APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed and JSON modes contact public IP lookup providers and may expose or return approximate location, ISP, and organization data.

Mitigation: Use simple mode when only the public IP address is needed, and avoid detailed lookups in sensitive contexts.

Risk: Results depend on third-party public IP lookup services and may be unavailable, rate-limited, or incomplete.

Mitigation: Treat lookup output as operational context and retry with another supported provider when the primary service fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shogunwin/skills/ip-query)
- [api.ipify.org lookup endpoint](https://api.ipify.org?format=json)
- [ipinfo.io lookup endpoint](https://ipinfo.io/json)
- [icanhazip.com lookup endpoint](https://icanhazip.com)
- [ifconfig.me lookup endpoint](https://ifconfig.me/ip)
- [ipecho.net lookup endpoint](https://ipecho.net/plain)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON results, commonly summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detailed and JSON modes may include approximate city, region, country, coordinates, postal code, timezone, ISP, and organization data when available.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
