## Description: <br>
Complete Polygon agent toolkit for session-based smart contract wallets, token operations, ERC-8004 on-chain identity and reputation, and x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesLawton](https://clawhub.ai/user/JamesLawton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and operate Polygon Agent Kit workflows, including wallet setup, session permissions, funding, token transfers, swaps, deposits, ERC-8004 registration, and x402 payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can auto-run external tunneling software and open a temporary public callback tunnel. <br>
Mitigation: Install only after reviewing and trusting the upstream code, pin or review the commit before use, and verify the complete approval URL before sharing it with the user. <br>
Risk: The workflow manages sensitive wallet session material, private keys, access keys, and encrypted session blobs. <br>
Mitigation: Use minimal wallet balances and tight session limits, never share private keys or session blobs in chats or logs, and delete temporary session files after import. <br>
Risk: On-chain write operations can transfer tokens, approve sessions, register agents, or execute deposits when broadcast. <br>
Mitigation: Keep dry-run previews as the default, require explicit --broadcast for writes, and verify recipient, amount, chain, contract, and session permissions before broadcasting. <br>


## Reference(s): <br>
- [Polygon Agents SDK on ClawHub](https://clawhub.ai/JamesLawton/polygon-agents-sdk) <br>
- [Polygon Agent Kit repository](https://github.com/0xPolygon/polygon-agent-kit) <br>
- [Polygon Agent Connector](https://agentconnect.polygon.technology/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, environment variables, CLI flags, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet approval, funding, transaction, troubleshooting, and security-handling instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
