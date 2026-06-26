## Description: <br>
Queries domestic flight information through the Juhe Data API using departure, arrival, and date inputs, then returns flight numbers, times, transfer details, and ticket prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer flight-search requests by extracting route and date inputs, converting cities to airport codes when needed, and querying Juhe for available flight options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details are sent to Juhe's third-party API. <br>
Mitigation: Only submit route and date details that are acceptable to share with Juhe. <br>
Risk: The Juhe API key can be exposed through command-line arguments, shell history, or committed .env files. <br>
Mitigation: Prefer JUHE_FLIGHT_KEY as an environment variable or managed secret, keep .env files out of version control, avoid passing --key when possible, and rotate exposed keys. <br>


## Reference(s): <br>
- [Juhe Flight Query API documentation](https://www.juhe.cn/docs/api/id/818) <br>
- [Juhe Data Platform](https://www.juhe.cn) <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-flight-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is formatted text followed by JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_FLIGHT_KEY; sends route and date queries to Juhe's flight API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
