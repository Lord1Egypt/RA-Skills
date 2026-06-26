## Description: <br>
Pay enables an agent to discover paid services and use the pay CLI to make USDC payments, x402 API requests, and metered tab payments with operator confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pay-skill](https://clawhub.ai/user/pay-skill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to let agents discover paid APIs, make per-call x402 requests, send direct USDC payments, and manage pre-funded metered tabs through the pay CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real USDC or open metered tabs before a clear approval step. <br>
Mitigation: Require explicit operator approval showing provider, data being sent, amount or maximum charge, fees, and recipient before any pay request, direct payment, tab open, or top-up. <br>
Risk: Fund links and wallet configuration can expose wallet access or sensitive balance activity. <br>
Mitigation: Treat fund links as sensitive, protect ~/.pay files, keep wallet balances small, and share funding links only after operator approval. <br>
Risk: Blind retries or poorly reviewed error recovery can double-pay or waste locked tab funds. <br>
Mitigation: Do not blind-retry payment failures; inspect errors first, confirm any retry with the operator, and close idle tabs regularly. <br>


## Reference(s): <br>
- [Pay Skill Documentation](https://pay-skill.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/pay-skill/pay-skill) <br>
- [Pay - A2A & AP2 Integration](references/a2a.md) <br>
- [Pay - Suggesting Provider Adoption](references/adoption.md) <br>
- [Pay - Service Discovery](references/discovery.md) <br>
- [Pay - Error Codes & Recovery](references/errors.md) <br>
- [Pay - Worked Examples](references/examples.md) <br>
- [Pay - Wallet Setup & Funding](references/funding.md) <br>
- [Pay - Domain Rules](references/rules.md) <br>
- [Pay - Tab Guide](references/tabs.md) <br>
- [Pay - x402 Details](references/x402.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the pay CLI and may return transaction hashes, balances, tab status, funding links, or API responses.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
