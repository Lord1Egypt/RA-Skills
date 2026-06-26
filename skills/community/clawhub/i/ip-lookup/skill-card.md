## Description: <br>
Investigate IP addresses and hostnames with geolocation, ASN and ISP details, reverse DNS, RDAP/WHOIS network information, and an optional AbuseIPDB reputation check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelZhangty](https://clawhub.ai/user/MichaelZhangty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and operators use this skill to inspect an IP address or hostname, identify network ownership and location signals, and optionally check AbuseIPDB reputation before further investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses or hostnames are sent to public lookup providers. <br>
Mitigation: Avoid using the skill for confidential internal infrastructure, customer indicators, or active incident-response targets unless that disclosure is approved. <br>
Risk: The optional AbuseIPDB check sends the queried IP address to AbuseIPDB when enabled. <br>
Mitigation: Set ABUSEIPDB_KEY and use the --abuse mode only when the reputation check is intentional and appropriate for the target. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/MichaelZhangty/ip-lookup) <br>
- [AbuseIPDB registration](https://www.abuseipdb.com/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal report or JSON from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live network lookups against public IP intelligence, DNS, RDAP, and optional AbuseIPDB services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
