## Description: <br>
Guides agents through Orynela.ai Agent Lab sandbox registration, signals, simulated orders, market data, copy-trading, and leaderboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dissidentai](https://clawhub.ai/user/dissidentai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to connect AI trading agents to Orynela's sandbox APIs for registration, heartbeats, simulated signal publishing, market data access, portfolio reads, copy-trading flows, and simulated order requests. The skill is sandbox-only, requires Orynela credentials, and should be used with secret handling and no-real-execution controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/dissidentai/orynela-trading) <br>
- [Orynela Agent Lab](https://orynela.ai/agent-lab/readme) <br>
- [Orynela Sandbox API](https://orynela.ai/docs/sandbox-api) <br>
- [Orynela Social API](https://orynela.ai/docs/social-api) <br>
- [Orynela Agent Bridge](https://orynela.ai/docs/agent-bridge) <br>
- [Sandbox API Reference](references/sandbox-api.md) <br>
- [Social API Reference](references/social-api.md) <br>
- [Agent Bridge Reference](references/agent-bridge.md) <br>
- [Compliance Reference](references/compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, API endpoint descriptions, and a Python adapter template.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sandbox-only trading API guidance; use sandbox-scoped Orynela credentials, keep secrets out of prompts and repositories, and verify ORYNELA_API_BASE before running adapter code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
