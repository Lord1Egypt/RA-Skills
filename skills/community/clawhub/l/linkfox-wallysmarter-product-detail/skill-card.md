## Description: <br>
This skill retrieves detailed Walmart product information via WallySmarter, including pricing history and sales volume trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce operators use this skill to look up a single Walmart Item ID and review product attributes, current price, price history, sales estimates, stock status, and listing quality signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Walmart product IDs and requests to LinkFox/WallySmarter using the user's LinkFox API key. <br>
Mitigation: Install and use the skill only when sharing those requests with LinkFox/WallySmarter is acceptable for the user's workflow. <br>
Risk: The security scan reports automatic feedback behavior that may send details about the user's statements and skill outcome to a separate LinkFox feedback endpoint. <br>
Mitigation: Review or disable the feedback behavior before use, and avoid sending sensitive user context through feedback. <br>


## Reference(s): <br>
- [WallySmarter Product Detail API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-wallysmarter-product-detail) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown summary with JSON API results from the helper script when invoked] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a Walmart productId; includeStats defaults to true.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
