## Description: <br>
Guides agents through buying API access with ProxyGate, including checking balances, depositing USDC, finding APIs, proxying requests, streaming responses, tracking usage, withdrawing funds, and rating sellers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to buy API access through ProxyGate and manage buyer-side CLI or SDK workflows. It is intended for balance checks, USDC deposits and withdrawals, API discovery, paid proxy requests, usage review, and seller ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent through financial and marketplace actions such as deposits, withdrawals, paid proxy requests, seller ratings, listing changes, tunnel exposure, or job marketplace actions. <br>
Mitigation: Require explicit user approval before each financial, paid-service, listing, tunnel, or marketplace action, and use a low-balance wallet or limited API key. <br>
Risk: Proxy requests may send secrets, personal data, proprietary payloads, or other sensitive information through third-party API services. <br>
Mitigation: Avoid sending sensitive data unless the selected service is intentionally trusted, and keep ProxyGate shield scanning enabled where appropriate. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ProxyGate CLI commands, SDK snippets, request payload examples, and operational checklists.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
