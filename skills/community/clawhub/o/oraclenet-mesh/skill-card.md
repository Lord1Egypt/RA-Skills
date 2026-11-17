## Description:

OracleNet routes AI agents to live external data and MCP capabilities for current blockchain, market, research, sanctions, weather, travel, and compliance-related tasks beyond the model's training cutoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooloracle](https://clawhub.ai/user/tooloracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task needs current external data or capability discovery and they need a route, price status, verification status, provenance, and limitations before acting. It is especially suited for free-first discovery across live data domains while keeping paid x402 calls behind explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A task intent can be sent to a non-ToolOracle HTTP(S) endpoint when the route script endpoint override is used.

Mitigation: Use the documented ToolOracle handshake endpoint by default and use an override only when the exact HTTPS destination is deliberately trusted.

Risk: Handshake intents are sent to ToolOracle and could expose sensitive or confidential information if the caller includes it.

Mitigation: Send only a minimal, nonsensitive routing summary; do not include secrets, personal data, wallet seed material, confidential business details, or full documents.

Risk: Paid x402 calls can spend funds if made without a clear budget and authorization.

Mitigation: Use free discovery first, present the quoted price, asset, and chain, and proceed only after explicit approval within a stated budget.

Risk: Live external data may be unsigned, stale, incomplete, or unsuitable as a final legal, financial, regulatory, or compliance decision.

Mitigation: Report provenance, timestamps, limitations, and verification status; verify signatures against the JWKS when a route declares signing and escalate consequential decisions to a human.

## Reference(s):

- [Route recipes](references/route-recipes.md)
- [Verification](references/verification.md)
- [x402 payment safety](references/x402-safety.md)
- [ToolOracle homepage](https://tooloracle.io)
- [OracleNet discovery card](https://tooloracle.io/.well-known/agent.json)
- [OracleNet handshake endpoint](https://tooloracle.io/handshake)
- [OracleNet MCP endpoint](https://tooloracle.io/quantum/mcp/)
- [OracleNet JWKS](https://tooloracle.io/.well-known/jwks.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON route summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint URLs, provenance, limitations, price status, and verification status; paid calls require explicit authorization.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
