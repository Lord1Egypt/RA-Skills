## Description: <br>
Queries the current device's public IP address and can optionally return geolocation and ISP details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shogunwin](https://clawhub.ai/user/shogunwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users invoke this skill when they need to see the machine's public IP address, with optional location and network-provider context for troubleshooting or network checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill contacts third-party public-IP and geolocation services that can observe the user's public IP address. <br>
Mitigation: Invoke it only when an IP lookup is intentional, and use detailed geolocation results only when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shogunwin/ip-query) <br>
- [ipify public IP API](https://api.ipify.org) <br>
- [ipinfo IP data API](https://ipinfo.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text or JSON, typically summarized for the user in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to public IP lookup services; curl is required and jq is optional for JSON parsing.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
