## Description: <br>
Accesses paid API endpoints and gated content using the x402 payment protocol and a Finance District wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to access x402 paid resources, inspect payment requirements, authorize a wallet payment, and return paid API or gated content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger could route ambiguous requests into wallet payment flows. <br>
Mitigation: Use the skill only for intended x402 paid resources, require a visible price and recipient preview, and personally confirm each spend before payment. <br>
Risk: Using a funded wallet for paid content can spend real assets if the requested endpoint or amount is unexpected. <br>
Mitigation: Use a dedicated low-balance wallet, check wallet balance first, set a maximum payment amount when possible, and inspect authorization details before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/pay-for-service-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fdx wallet commands for status, balance checks, x402 content retrieval, and payment authorization.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
