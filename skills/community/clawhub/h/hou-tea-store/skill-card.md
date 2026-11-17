## Description:

Browse, recommend, and purchase Chinese tea from hou-tea.com using the agent-native API (https://hou-tea.com/api/agent/catalog) and x402 USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackrain19743](https://clawhub.ai/user/jackrain19743)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to browse live Chinese tea products, request recommendations, compare product details, and initiate purchases through hou-tea.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tea queries may be sent to a third-party merchant API.

Mitigation: Use the skill only when interaction with hou-tea.com is intended, and avoid sending sensitive or unrelated personal details in recommendation requests.

Risk: The skill can guide x402 USDC payment flows for purchases.

Mitigation: Before authorizing payment, independently verify the product, amount, recipient address, USDC token contract, Base network, and wallet prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackrain19743/skills/hou-tea-store)
- [Hou Tea agent catalog API](https://hou-tea.com/api/agent/catalog)
- [Hou Tea recommendation API](https://hou-tea.com/api/agent/recommend)
- [Hou Tea payment API](https://hou-tea.com/pay/api/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with API request examples and product recommendation cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product recommendations must be based on live API responses, and payment guidance is limited to x402 USDC purchase flows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
