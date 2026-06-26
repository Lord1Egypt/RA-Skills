## Description: <br>
Automatically retrieves IP geolocation and network information for a specified IP address or the current public IP using the free ip-api.com service without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likwang](https://clawhub.ai/user/likwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security analysts use this skill to check estimated location, ISP, organization, AS number, and related network fields for public IP addresses during troubleshooting, log review, or lightweight network investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses, and the user's current public IP when no address is provided, are sent to ip-api.com over unencrypted HTTP. <br>
Mitigation: Avoid sensitive investigations or confidential network targets unless the provider or transport is replaced with a privacy-reviewed HTTPS option. <br>
Risk: Returned geolocation is estimated and unsuitable for street-level location or high-assurance attribution. <br>
Mitigation: Use results as contextual network information and corroborate with other sources before making security or operational decisions. <br>


## Reference(s): <br>
- [ip-api.com API documentation](https://ip-api.com/docs/) <br>
- [ip-api.com service page](https://ip-api.com/) <br>
- [API field reference](references/fields.md) <br>
- [ClawHub skill page](https://clawhub.ai/likwang/ip-locator-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON or formatted text lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lookup output is based on ip-api.com responses and may include estimated location, coordinates, timezone, ISP, organization, AS number, and queried IP.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
