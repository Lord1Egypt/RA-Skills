## Description: <br>
Check IP address threat intelligence. Query multiple sources for IP reputation, geolocation, and threat scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeter226](https://clawhub.ai/user/freeter226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and developers use this skill to check individual or bulk IP addresses for geolocation, network ownership, and reputation signals during log review, triage, or threat hunting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses, including entries from bulk files, are sent to external lookup services. <br>
Mitigation: Use only with indicators approved for third-party sharing, and avoid confidential customer, internal, or incident-response data unless that sharing is approved. <br>
Risk: AbuseIPDB checks require an API key. <br>
Mitigation: Provide a limited AbuseIPDB API key through ABUSEIPDB_API_KEY and avoid storing the key in files or command history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freeter226/ip-threat-check) <br>
- [ip-api.com lookup endpoint](http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,isp,org,as,asname,query) <br>
- [AbuseIPDB check endpoint](https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays={days}) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON results with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. AbuseIPDB checks use ABUSEIPDB_API_KEY when configured; basic geolocation queries use an external IP lookup service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
