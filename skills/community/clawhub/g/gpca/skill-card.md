## Description: <br>
Manage GPCA bank cards, USDT wallet, KYC verification, and automate shopping on Amazon/Taobao with browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lobclaw](https://clawhub.ai/user/lobclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage GPCA cards, USDT wallet funds, KYC workflows, and assisted purchases through browser automation. It is intended for agent-driven financial and shopping workflows that require explicit user confirmation for transfers, card changes, payment data use, and purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run remote MCP server code. <br>
Mitigation: Install only after trusting the publisher and reviewing or isolating the remote MCP server repository and setup commands. <br>
Risk: The skill can access email inbox pages to retrieve verification codes. <br>
Mitigation: Prefer manual verification code entry; if browser access is used, restrict processing to GPCA verification emails and avoid granting broad inbox access. <br>
Risk: The skill handles financial operations, card details, KYC documents, and purchases. <br>
Mitigation: Require explicit confirmation for every transfer, card change, KYC upload, CVV/PIN action, and purchase, and never allow automatic retries for ambiguous transfers. <br>


## Reference(s): <br>
- [GPCA skill page](https://clawhub.ai/lobclaw/gpca) <br>
- [GPCA skill repository](https://github.com/gpcaclaw/gpca-skill) <br>
- [GPCA MCP server repository](https://github.com/gpcaclaw/gpca-mcp-server.git) <br>
- [GPCA MCP Tools Reference](references/api-reference.md) <br>
- [Card Manager - Detailed Workflows](references/card-manager.md) <br>
- [Security & Privacy Guidelines](references/security-notes.md) <br>
- [Shopping Assistant - Detailed Workflows](references/shopping-assistant.md) <br>
- [Shopping Flows & Site-Specific Tips](references/shopping-flows.md) <br>
- [Common User Flows](references/user-flows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API Calls, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions, MCP setup, GPCA account workflows, card and wallet operations, KYC steps, and shopping confirmations.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
