## Description: <br>
Shop autonomously on Amazon via Moltpho - search products, manage credit, and purchase items using mUSD on Base mainnet <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unifiedh](https://clawhub.ai/user/unifiedh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use Moltpho to search Amazon products, manage credit, maintain shipping setup, and place orders through the Moltpho API and browser portal. The skill is intended for shopping workflows that may include autonomous or proactive purchasing when owner settings allow it. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Moltpho can place real Amazon orders and spend credit from inferred conversation needs without a fresh confirmation by default. <br>
Mitigation: Disable proactive purchasing unless it is deliberately needed, enable confirmation-required mode, and set strict per-order and daily spending caps before use. <br>
Risk: The skill stores local Moltpho API credentials that can authorize account actions. <br>
Mitigation: Protect the local credentials file, keep owner-sensitive payment and shipping changes in the portal, and remove local credentials with logout when the agent should no longer act. <br>
Risk: Purchases may be made for unwanted or disallowed categories if owner controls are not configured carefully. <br>
Mitigation: Configure denylists or allowlists and rely on confirmation-required mode for purchases outside routine low-risk categories. <br>


## Reference(s): <br>
- [Moltpho ClawHub page](https://clawhub.ai/unifiedh/moltpho) <br>
- [Moltpho API Reference](artifact/references/API.md) <br>
- [Moltpho Purchasing Policies](artifact/references/POLICIES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured status text with API request and response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local credentials file and may open the Moltpho browser portal for owner-controlled setup, payment, shipping, and order management.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
