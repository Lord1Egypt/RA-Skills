## Description: <br>
Queries current China oil prices for 92, 95, and 98 octane gasoline and 0 diesel by province or city using the Juhe API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer oil-price questions for China, either nationwide or filtered to a province or city, and present the latest returned prices in a table or JSON. <br>

### Deployment Geography for Use: <br>
Global (data coverage is China oil-price data). <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Juhe API key for oil-price lookups, and documented configuration options include plaintext .env storage or passing the key on the command line. <br>
Mitigation: Prefer the JUHE_OIL_KEY environment variable, avoid passing the key with --key, and do not commit scripts/.env. <br>
Risk: The script queries an HTTP API URL, which may expose requests on networks that do not protect transport. <br>
Mitigation: Consider changing the API URL to HTTPS if Juhe supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-oil-price) <br>
- [Juhe oil price API documentation](https://www.juhe.cn/docs/api/id/540) <br>
- [Juhe data platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and table or JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Juhe API key, normally supplied through the JUHE_OIL_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
