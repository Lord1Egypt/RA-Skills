## Description: <br>
Queries IPv4 geolocation details such as country, province, city, and ISP through the Juhe IP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jenius-cn](https://clawhub.ai/user/jenius-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up IPv4 address ownership and location details for single IPs or small batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script sends the Juhe API key and queried IP address over plain HTTP. <br>
Mitigation: Review before installing, query only IP addresses approved for sharing with Juhe, and change the endpoint to HTTPS before using a real Juhe API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jenius-cn/juhe-ip-query) <br>
- [Juhe IP geolocation API documentation](https://www.juhe.cn/docs/api/id/1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output as text lines, tables, and JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_IP_KEY; supports single or multiple IPv4 address inputs.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
