## Description: <br>
Monitor and report usage, costs, quotas, and rate limits for LLM providers, plus manage clawmeter setup and daemon status securely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielithomas](https://clawhub.ai/user/danielithomas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check LLM usage, costs, quotas, rate limits, provider status, and clawmeter setup from an agent session. It helps summarize current and historical usage while guiding secure local configuration and daemon management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose local package installation, daemon start, systemd service installation, or history purge actions. <br>
Mitigation: Review prompts carefully and require explicit user approval before approving package installation, daemon management, systemd service installation, or destructive history purge commands. <br>
Risk: Credential exposure could occur if a user pastes API keys, tokens, or credential contents into chat. <br>
Mitigation: Do not paste API keys into chat; configure credentials directly in local clawmeter setup and rotate any secret shared in conversation. <br>
Risk: Usage, quota, and cost data can be sensitive operational information. <br>
Mitigation: Run only the intended local clawmeter queries and keep responses limited to the usage details requested by the user. <br>


## Reference(s): <br>
- [LLM Monitor on ClawHub](https://clawhub.ai/danielithomas/llm-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/danielithomas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise prose, tables or lists when useful, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON output from local clawmeter commands; does not handle credential values.] <br>

## Skill Version(s): <br>
0.7.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
