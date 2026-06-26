## Description: <br>
IPinfo (ipinfo.io) helps agents search and read IP intelligence through OOMOL's IPinfo connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to retrieve IPinfo data through an OOMOL-connected account, including current-IP lookups, arbitrary-IP geolocation, hostname, organization, company, carrier, abuse contact, privacy, token metadata, batch lookup, and map report actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP lookup requests, current-IP actions, bulk map uploads, and token metadata requests route data through OOMOL and IPinfo. <br>
Mitigation: Use the skill only when sharing those IP addresses or account metadata with OOMOL/IPinfo is intended, and avoid sensitive networks or large private IP lists unless the service handling terms have been reviewed. <br>


## Reference(s): <br>
- [IPinfo ClawHub Skill](https://clawhub.ai/oomol/oo-ipinfo-io) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [IPinfo Homepage](https://ipinfo.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return IPinfo connector responses containing IP intelligence data and OOMOL execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
