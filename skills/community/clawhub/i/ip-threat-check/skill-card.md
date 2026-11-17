## Description:

Check IP address threat intelligence. Query multiple sources for IP reputation, geolocation, and threat scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeter226](https://clawhub.ai/user/freeter226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill to check suspicious IPs, enrich log analysis, support incident response, and perform threat hunting with IP reputation and geolocation data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IP addresses, including bulk file contents, are submitted to external services.

Mitigation: Use the skill only for IPs that are approved for external reputation checks, and avoid sensitive internal or customer IP lists unless disclosure is acceptable.

Risk: Bulk checks can disclose many addresses in one run.

Mitigation: Review bulk files before execution and limit them to the smallest necessary investigation scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeter226/skills/ip-threat-check)
- [freeter226 Publisher Profile](https://clawhub.ai/user/freeter226)
- [ip-api.com lookup endpoint](http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,isp,org,as,asname,query)
- [AbuseIPDB check endpoint](https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays={days})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script returns JSON containing geolocation, network, source status, threat score, report count, and risk level when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
