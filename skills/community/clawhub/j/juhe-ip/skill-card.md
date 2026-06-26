## Description: <br>
Queries IPv4 geolocation details including country, province, city, and ISP through the Juhe IP lookup API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up the geographic and ISP attribution for one or more public IPv4 addresses. It can return natural-language summaries, table output, and JSON results for IP investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the script sends the API key and queried public IPs over unencrypted HTTP. <br>
Mitigation: Change the Juhe API endpoint to HTTPS before use if Juhe supports it, and only query IP addresses that are acceptable to send to Juhe. <br>
Risk: The skill requires a Juhe API key. <br>
Mitigation: Treat JUHE_IP_KEY like a password, prefer environment variable or local .env configuration, and avoid passing the key on the command line. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-ip) <br>
- [Juhe IP lookup API documentation](https://www.juhe.cn/docs/api/id/1) <br>
- [Juhe data services](https://www.juhe.cn) <br>
- [Juhe IP API endpoint](http://apis.juhe.cn/ip/ipNewV3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, API Calls, Guidance] <br>
**Output Format:** [Natural language, terminal table output, and JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_IP_KEY for API-backed lookups; supports single and batch IPv4 queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
