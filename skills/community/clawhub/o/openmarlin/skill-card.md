## Description: <br>
Use OpenMarlin from OpenClaw to answer questions, run tasks, and manage OpenMarlin account setup and billing flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex4506](https://clawhub.ai/user/alex4506) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to access OpenMarlin from OpenClaw for account registration, API key bootstrap, execution requests, long-running task submission, and billing or top-up recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles billing authority, top-up flows, account setup, and referral information. <br>
Mitigation: Install only when the OpenMarlin API origin is trusted and review billing actions before approving external checkout or account changes. <br>
Risk: Registration bootstrap can expose newly issued API keys in command output or logs. <br>
Mitigation: Run registration and bootstrap in a private context, avoid sharing terminal or agent logs, and use local credential storage only when intentionally saving the key. <br>
Risk: The server-resolved security verdict is suspicious. <br>
Mitigation: Review the skill and scan results before deployment, especially credential handling and purchase-related flows. <br>


## Reference(s): <br>
- [ClawHub OpenMarlin release page](https://clawhub.ai/alex4506/openmarlin) <br>
- [OpenMarlin website](https://openmarlin.ai) <br>
- [OpenMarlin API origin](https://api.openmarlin.ai) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide OpenClaw API calls for registration, executions, asynchronous tasks, billing, and top-up recovery.] <br>

## Skill Version(s): <br>
0.1.22-main.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
