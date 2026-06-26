## Description: <br>
SMS verification and virtual phone numbers via Grizzly SMS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grizzlysms-git](https://clawhub.ai/user/grizzlysms-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to integrate Grizzly SMS number rental, balance checks, pricing lookup, SMS polling, and activation status updates into agent workflows. It can also guide setup for MCP or OpenClaw skill execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through third-party account registration with rented phone numbers. <br>
Mitigation: Use only for lawful, policy-compliant verification workflows with explicit authorization; avoid automated account creation or platform-rule evasion. <br>
Risk: API keys and SMS codes may be pasted into chat, stored in config, or exposed through bundled API examples. <br>
Mitigation: Use a protected secret store, avoid long-lived credentials in conversations, and rotate any key exposed in bundled examples or configuration files. <br>
Risk: The skill can retrieve a crypto wallet address for balance top-up. <br>
Mitigation: Verify payment details directly with Grizzly SMS before sending funds; the agent should only display provider responses and should not execute transactions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/grizzlysms-git/grizzly-sms-mcp) <br>
- [Grizzly SMS API documentation](https://grizzlysms.com/docs) <br>
- [Grizzly SMS website](https://grizzlysms.com/) <br>
- [README](README.md) <br>
- [OpenClaw configuration guide](CONFIG.md) <br>
- [Bundled Grizzly SMS API protocol](docs/api-protocol-for-working-with-grizzly-sms.json) <br>
- [Bundled services catalog](docs/services.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JSON snippets, and API-derived values such as phone numbers, activation IDs, balances, wallet addresses, and SMS codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive identifiers or credentials supplied by the user; handle API keys and SMS codes as secrets.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
