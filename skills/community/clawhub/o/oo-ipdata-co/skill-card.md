## Description: <br>
The ipdata.co skill lets an agent use the OOMOL oo CLI connector to look up IP geolocation, ASN, carrier, company, currency, language, time zone, and threat data from ipdata.co. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent inspect the live ipdata.co connector schema and run read-only IP intelligence lookups through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP addresses submitted for lookup, including current-IP requests, are processed through the OOMOL connector layer and ipdata.co. <br>
Mitigation: Use the skill only for IP lookup data that is appropriate to share with the connected services, and avoid submitting sensitive addresses unless that processing is acceptable. <br>
Risk: First-time setup may require installing the oo CLI before the connector can run. <br>
Mitigation: Verify the oo CLI installer source before running setup commands. <br>


## Reference(s): <br>
- [ipdata.co homepage](https://ipdata.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
