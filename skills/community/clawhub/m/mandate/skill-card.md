## Description: <br>
Mandate helps agents enforce wallet spend limits, validate transactions before signing, configure allowlists and approvals, detect prompt injection in transaction reasoning, scan for unprotected wallet calls, and audit transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftadviser](https://clawhub.ai/user/swiftadviser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Mandate to add a policy gate before wallet transfers, swaps, purchases, and other spend-bearing actions. The skill provides validation, registration, scanner, MCP, REST, and plugin integration guidance for agent wallet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet transaction metadata and requires a Mandate runtime key for authenticated use. <br>
Mitigation: Protect MANDATE_RUNTIME_KEY, avoid logging it, restrict credential-file permissions, and rotate the key if exposure is suspected. <br>
Risk: Transactions can bypass configured spend limits and approvals if an agent skips validation before wallet execution. <br>
Mitigation: Call Mandate validation before every spend-bearing wallet action and halt execution when validation fails or the policy service is unreachable. <br>
Risk: Transaction reasons and metadata are sent to Mandate and logged for audit. <br>
Mitigation: Use concise transaction reasons, avoid unnecessary sensitive data, and use anonymous heartbeat checks unless activity tracking is desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/swiftadviser/mandate) <br>
- [Mandate App](https://app.mandate.md) <br>
- [Mandate MCP Server](https://mcp.mandate.md/mcp) <br>
- [Claude Mandate Plugin](https://github.com/SwiftAdviser/claude-mandate-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with CLI, REST, SDK, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MANDATE_RUNTIME_KEY for authenticated runtime use; some flows can use x402 pay-per-call instead.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
