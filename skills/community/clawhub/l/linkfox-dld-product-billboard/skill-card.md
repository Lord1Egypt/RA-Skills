## Description: <br>
Helps agents query 1688 product bestseller rankings for wholesale sourcing and product research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, sourcing researchers, and commerce operators use this skill to discover and compare 1688 wholesale products by weekly or monthly bestseller ranking, supplier, price, sales volume, and dropshipping filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends 1688 sourcing queries and filters to LinkFox using a LinkFox API key. <br>
Mitigation: Use it only for queries that are acceptable to share with LinkFox, and avoid confidential sourcing plans, credentials, or private business details. <br>
Risk: The artifact instructs the agent to silently post feedback about user intent or satisfaction to a separate LinkFox feedback API. <br>
Mitigation: Require explicit operator approval for feedback submission or remove that behavior before deployment. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-dld-product-billboard) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and formatted product summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw JSON API responses, product and shop URLs, pricing, sales metrics, supplier names, and product image URLs when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
