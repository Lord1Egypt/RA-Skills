## Description: <br>
Mint (purchase) an Art Blocks token using the artblocks-mcp tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryley-o](https://clawhub.ai/user/ryley-o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Art Blocks minting details, check eligibility for gated projects, understand minter mechanics, and prepare supported purchase transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may sign a transaction for the wrong Art Blocks project, chain, price, or recipient. <br>
Mitigation: Confirm the project ID, chain, ETH price, recipient or purchaseTo address, and all warnings before wallet signing. <br>
Risk: The skill relies on the configured artblocks-mcp provider for project, eligibility, and transaction information. <br>
Mitigation: Use the skill only with a trusted artblocks-mcp provider and verify generated transaction details independently before signing. <br>
Risk: Allowlist and profile eligibility checks can expose linked wallet information. <br>
Mitigation: Treat wallet, profile, and eligibility results as private information and avoid sharing them beyond the minting workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryley-o/mint-artblocks-token) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown with structured tool-use guidance and transaction details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces minting guidance, eligibility-check instructions, warnings to surface before signing, and supported transaction-building details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
