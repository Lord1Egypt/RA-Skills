## Description: <br>
Browse, recommend, and purchase Chinese tea from hou-tea.com using the agent-native catalog and recommendation APIs with x402 USDC payment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackrain19743](https://clawhub.ai/user/jackrain19743) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to browse real tea catalog data, receive tea recommendations, compare products, and prepare purchases from hou-tea.com. The skill is intended for product discovery and purchase flows where an agent must use live API responses instead of cached or invented product details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent into real x402 USDC payment flows. <br>
Mitigation: Before enabling any wallet or ordering credentials, require a separate final confirmation showing the product, quantity, total USDC amount, Base network, recipient address, and that real funds may be spent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackrain19743/hou-tea-store) <br>
- [Hou Tea Agent Catalog API](https://hou-tea.com/api/agent/catalog) <br>
- [Hou Tea Agent Recommendation API](https://hou-tea.com/api/agent/recommend) <br>
- [Hou Tea x402 Purchase API](https://hou-tea.com/pay/api/v1/buy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown product recommendations and purchase guidance with API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product images, product links, x402 payment details, and confirmation guidance when supported by live API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
