## Description:

Looks up geolocation and network information for a specified IP address or the current public IP using ip-api.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likwang](https://clawhub.ai/user/likwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security analysts can use this skill to inspect public IP address location, ISP, organization, ASN, and timezone details during troubleshooting or log review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IP addresses, and possibly the user's own public IP, are sent to ip-api.com.

Mitigation: Avoid using the skill for confidential investigations or sensitive customer data unless disclosure to that service is acceptable.

Risk: The artifact uses plain HTTP for ip-api.com requests.

Mitigation: Use an HTTPS-capable provider or modify the skill before handling sensitive lookups.

Risk: Returned geolocation is approximate and may be unsuitable for precise location decisions.

Mitigation: Treat location results as coarse network intelligence and verify with additional sources before acting on them.

## Reference(s):

- [ip-api.com API documentation](https://ip-api.com/docs/)
- [ip-api.com API field reference](references/fields.md)
- [ip-api.com service site](https://ip-api.com/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and formatted command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call ip-api.com to return approximate geolocation and network metadata for one or more IP addresses.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
