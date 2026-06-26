## Description: <br>
Perform IP geolocation lookups with the ipinfo.io API to convert IP addresses into geographic and network data such as city, region, country, postal code, timezone, coordinates, and organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiagom101](https://clawhub.ai/user/tiagom101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to look up geographic and network metadata for IP addresses, enrich IP lists, and extract fields such as country, city, timezone, coordinates, and organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP addresses submitted for lookup are sent to ipinfo.io. <br>
Mitigation: Only look up IP addresses that are acceptable to share with ipinfo.io under the user's data handling requirements. <br>
Risk: An IPINFO_TOKEN can be exposed if pasted directly into URLs or shared prompts. <br>
Mitigation: Configure IPINFO_TOKEN through the dashboard or environment variable and avoid embedding real tokens in prompts, logs, or reusable examples. <br>


## Reference(s): <br>
- [IPinfo homepage](https://ipinfo.io) <br>
- [ClawHub IPinfo skill page](https://clawhub.ai/tiagom101/ipinfo) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for optional IPINFO_TOKEN configuration and JSON field extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
