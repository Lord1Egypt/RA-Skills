## Description:

Looks up IP geolocation, public IP details, reverse DNS, ISP/ASN data, and bulk IP location records using free lookup APIs with no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run IP geolocation checks, find the current public IP address, inspect ISP/ASN and reverse DNS data, and process small batches of IPs from a file or standard input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup targets, domains, and the user's public IP may be sent to external lookup services.

Mitigation: Avoid using the skill for sensitive asset inventories unless the lookup provider and data handling are approved.

Risk: The main geolocation API uses plaintext HTTP.

Mitigation: Use an HTTPS geolocation provider before relying on the skill for sensitive or production network data.

Risk: Input validation is permissive and accepts IP-like strings or domains.

Mitigation: Add stricter validation if the skill will process untrusted bulk input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/ip-geo-toolkit)
- [ipify public IP API endpoint](https://api.ipify.org?format=json)
- [ip-api.com single lookup endpoint](http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query)
- [ip-api.com batch lookup endpoint](http://ip-api.com/batch?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [Plain text or JSON command output, with optional file output for bulk lookups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bulk mode processes up to 100 IPs per batch; lookups send queried IPs or domains to external services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
