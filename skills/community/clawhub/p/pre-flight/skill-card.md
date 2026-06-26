## Description: <br>
Stop your agent from doing things you didn't authorize. ICME checks every consequential action against your policy before it executes -- email, transactions, file ops, external calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyattbenno777](https://clawhub.ai/user/wyattbenno777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Pre Flight to check consequential agent actions against ICME policies before execution, block actions that violate policy, and screen multi-step plans for contradictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends proposed actions, policy details, reasoning summaries, and audit metadata to ICME. <br>
Mitigation: Avoid including secrets or unnecessary internal details in action descriptions or policies, and protect the ICME API key. <br>
Risk: The guardrail is advisory unless the runtime enforces mandatory checks and fail-closed behavior. <br>
Mitigation: Require checks before consequential actions and treat API failures, malformed responses, or any result other than explicit approval as blocked. <br>
Risk: Paid x402, agentcash, signup, and top-up flows can spend funds automatically if left uncapped. <br>
Mitigation: Disable or tightly cap paid flows and require human approval for signup, top-ups, and per-call payments. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/wyattbenno777/pre-flight) <br>
- [ICME documentation](https://docs.icme.io/documentation) <br>
- [ICME API reference](https://docs.icme.io/api-reference) <br>
- [Relevance Screening](https://docs.icme.io/documentation/learning/relevance-screening) <br>
- [Battle Testing Rules](https://docs.icme.io/documentation/battle-testing-rules) <br>
- [Succinctly Verifiable Agentic Guardrails](https://arxiv.org/abs/2602.17452) <br>
- [MCP Server (npm)](https://www.npmjs.com/package/icme-preflight-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with curl examples and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated checks require ICME_API_KEY and ICME_POLICY_ID; checkLogic can be used without an account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and target metadata; artifact _meta.json lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
