## Description: <br>
Ip Geo Toolkit helps agents look up IP geolocation, public IP, ISP/ASN, and reverse DNS data and run bulk IP lookups using free APIs without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security analysts use this skill to inspect public IP addresses, domains, or lists of IPs for location, network ownership, ASN, and reverse DNS context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IPs, domains, and bulk IP lists are sent to third-party lookup services such as ip-api.com and ipify, including HTTP geolocation traffic. <br>
Mitigation: Use the skill only when sharing those addresses with the external services is acceptable, and avoid confidential customer, incident-response, or internal infrastructure lists unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/ip-geo-toolkit) <br>
- [ip-api.com lookup API](http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query) <br>
- [ipify public IP API](https://api.ipify.org?format=json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files] <br>
**Output Format:** [Plain text or JSON command output, with optional output files for bulk lookup results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes up to 100 IPs per batch and may write bulk results to a requested output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
