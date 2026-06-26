## Description: <br>
Use the GSData open platform through a local adapter script for account, content, ranking, public sentiment, and NLP queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyuwen-bri](https://clawhub.ai/user/yangyuwen-bri) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to let an agent query GSData for public sentiment monitoring, hot events, platform rankings, account data, content search, and NLP results using GSData credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses GSData credentials to call the GSData platform. <br>
Mitigation: Install only for trusted agents and use least-privilege GSData keys stored in environment variables or a controlled credentials file. <br>
Risk: The adapter exposes write-like, admin, and raw-route API abilities beyond simple lookup. <br>
Mitigation: Run dry-runs first, avoid broad automatic activation, and review every raw-route or --allow-write command before execution. <br>
Risk: The bundled default API endpoint uses HTTP. <br>
Mitigation: Use an HTTPS GSData endpoint if the service supports it, especially when sending sensitive parameters or credentials-derived requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangyuwen-bri/gsdata-skill) <br>
- [GSData API service endpoint](http://databus.gsdata.cn:8888/api/service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summarized GSData API results; large responses should be limited and paginated.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
