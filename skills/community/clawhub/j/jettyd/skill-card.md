## Description: <br>
Interact with IoT devices via the jettyd platform: read sensors, send commands, manage rules, and list devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jettydiot](https://clawhub.ai/user/jettydiot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT operators use this skill to let an agent inspect jettyd-connected devices, read current and historical telemetry, send device commands, and configure rules or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control real IoT devices and persistent automations. <br>
Mitigation: Require explicit human approval before relay, actuator, irrigation, power, configuration, or webhook changes. <br>
Risk: The skill requires sensitive jettyd credentials. <br>
Mitigation: Use least-privilege API keys, store credentials outside committed files, and rotate keys if exposure is suspected. <br>
Risk: Rules and webhooks can persist after the initial agent session. <br>
Mitigation: Periodically review active rules and webhooks for unexpected persistence. <br>


## Reference(s): <br>
- [Jettyd Skill Page](https://clawhub.ai/jettydiot/jettyd) <br>
- [Jettyd Publisher Profile](https://clawhub.ai/user/jettydiot) <br>
- [Jettyd Homepage](https://jettyd.com) <br>
- [Jettyd API Base](https://api.jettyd.com/v1) <br>
- [API Summary](references/api-summary.md) <br>
- [LangChain Example](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and API-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute authenticated API interactions with the jettyd platform when configured with a valid API key.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
