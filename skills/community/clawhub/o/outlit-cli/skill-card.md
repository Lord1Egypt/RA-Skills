## Description: <br>
Use when running Outlit CLI commands, setting up Outlit for AI agents, authenticating with Outlit, querying customer data from the terminal, or troubleshooting Outlit CLI issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafa-thayto](https://clawhub.ai/user/rafa-thayto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and customer-facing teams use this skill to run the Outlit CLI for customer intelligence workflows, including authentication, customer and user lookup, timeline review, natural language search, SQL analytics, and AI agent setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to access sensitive Outlit customer data. <br>
Mitigation: Install it only for agents that should access Outlit customer data and keep customer, SQL, and search queries limited to the task. <br>
Risk: API keys may be exposed if real keys are placed directly in commands or logs. <br>
Mitigation: Prefer a secure secret manager, scoped environment injection, or stored credentials over embedding real keys in command text. <br>
Risk: Automatic agent setup may apply broader configuration changes than intended. <br>
Mitigation: Review any outlit setup --yes changes before applying them broadly. <br>


## Reference(s): <br>
- [Outlit Cli on ClawHub](https://clawhub.ai/rafa-thayto/outlit-cli) <br>
- [Publisher profile: rafa-thayto](https://clawhub.ai/user/rafa-thayto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to produce or request JSON output from the Outlit CLI when stdout is piped or --json is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
