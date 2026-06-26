## Description: <br>
PayMe helps agents connect to PayMe smart wallets, check USDC/USDT balances, prepare stablecoin payments, view transaction history, manage contacts, and support P2P crypto-to-local-currency sells. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[variousfoot](https://clawhub.ai/user/variousfoot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect PayMe wallet state, prepare stablecoin transfers, manage contacts, and help sell USDC/USDT for local currency through PayMe's P2P flow after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global for wallet and payment assistance; P2P sell flows are documented for Nigeria, Ghana, Kenya, South Africa, Cameroon, Senegal, Benin, Togo, Tanzania, and Uganda. <br>

## Known Risks and Mitigations: <br>
Risk: Agent tokens grant limited wallet authority and could enable wallet activity if stored or exposed improperly. <br>
Mitigation: Store tokens only in an encrypted secrets store or other protected local mechanism, never log or commit them, prefer short token durations, and revoke access when finished. <br>
Risk: Stablecoin payments or P2P sell orders can move funds and may be difficult or impossible to reverse after confirmation. <br>
Mitigation: Use the default two-step flow, show a fresh preview with fees and recipient or local-currency details, and require explicit user approval before confirming any transfer or sell. <br>
Risk: P2P escrow can auto-release after the vendor marks fiat as sent, even if the user has not verified receipt. <br>
Mitigation: Prompt the user to check their bank or mobile money immediately, only confirm after they verify receipt, and direct them to open a dispute before auto-release if funds have not arrived. <br>


## Reference(s): <br>
- [PayMe Web App](https://payme.feedom.tech) <br>
- [PayMe Agent API Reference](references/api-reference.md) <br>
- [PayMe Agent API](https://api.feedom.tech) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API endpoint examples and JSON request/response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing payment previews, connection steps, and operational guidance; the skill itself contains instructions and configuration, not executable code.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
