## Description: <br>
Helps agents configure MoonPay Commerce (Helio) credentials and manage Solana crypto payment flows by listing currencies, creating Pay Links, generating checkout URLs, and checking transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mavagio](https://clawhub.ai/user/mavagio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and merchants use this skill to set up MoonPay Commerce credentials and manage Solana crypto payment links from an agent-assisted workflow. It is useful for creating payment links or checkout URLs, listing supported currencies, and reviewing payment transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and status commands can expose MoonPay Commerce API credential material in terminal output. <br>
Mitigation: Run setup only in a trusted local terminal, avoid sharing terminal logs or screenshots, and clear the saved config when finished. <br>
Risk: The skill can create, charge, disable, or enable payment links for a merchant account. <br>
Mitigation: Use a dedicated least-privilege API key if available, and verify amounts, currency symbols, wallet IDs, and pay link IDs before running create or disable actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mavagio/mpc-accept-crypto-payments) <br>
- [MoonPay Commerce API Reference](references/api-reference.md) <br>
- [Helio OpenAPI](https://api.hel.io/v1/docs-json) <br>
- [Helio Documentation](https://docs.hel.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, curl, HELIO_API_KEY, HELIO_API_SECRET, and local credential storage at ~/.mpc/helio/config with mode 600.] <br>

## Skill Version(s): <br>
0.3.0 (source: release evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
