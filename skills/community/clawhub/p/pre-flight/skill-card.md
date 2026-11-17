## Description:

Pre Flight helps agents check consequential actions against an ICME policy before execution, covering actions such as email, transactions, file operations, and external calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyattbenno777](https://clawhub.ai/user/wyattbenno777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Pre Flight to require policy checks before agents take consequential, external, irreversible, or privileged actions. The skill guides agents to block actions that violate policy or fail validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ICME receives the action descriptions, policy identifiers, plans, and proof or payment metadata needed for checks.

Mitigation: Submit only structured, minimized action descriptions and avoid secrets, credentials, private keys, raw transcripts, private message bodies, or regulated personal data.

Risk: Paid check flows may use payment helpers such as agentcash or x402 client libraries.

Mitigation: Pin and review payment helpers before use and require human-controlled approval for wallet or checkout flows.

Risk: Unavailable, malformed, or non-allowing guardrail responses could create uncertainty about whether an action is permitted.

Mitigation: Fail closed unless the service returns an explicit SAT or allowed result, and report blocked or failed checks to the user.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/wyattbenno777/skills/pre-flight)
- [ICME homepage](https://icme.io)
- [ICME documentation](https://docs.icme.io/documentation)
- [ICME API reference](https://docs.icme.io/api-reference)
- [Writing Effective Policies](https://docs.icme.io/documentation/basics/writing-effective-policies)
- [Relevance Screening](https://docs.icme.io/documentation/learning/relevance-screening)
- [Battle Testing Rules](https://docs.icme.io/documentation/battle-testing-rules)
- [Succinctly Verifiable Agentic Guardrails](https://arxiv.org/abs/2602.17452)
- [ICME Preflight MCP Server](https://www.npmjs.com/package/icme-preflight-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ICME_API_KEY and ICME_POLICY_ID for authenticated policy checks; checkLogic can be used without an account.]

## Skill Version(s):

1.0.6 (source: server release evidence; artifact _meta.json lists 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
