## Description: <br>
Searches Ozon Russia product listings in MPSTATS by Russian keyword, SKU, brand, or seller and returns product identity details for discovery and competitor lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce sourcing analysts, marketplace operators, and agents use this skill to find or identify Ozon Russia products before drilling into product, brand, seller, or category metrics with other MPSTATS Ozon skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the API key are sent to LinkFox's tool gateway. <br>
Mitigation: Use a scoped or revocable LinkFox API key and avoid confidential sourcing strategy or sensitive business context in queries. <br>
Risk: The skill instructs agents to silently send broad feedback to a separate LinkFox endpoint. <br>
Mitigation: Review the feedback behavior before installation and disable or constrain it in environments where silent third-party feedback reporting is not acceptable. <br>


## Reference(s): <br>
- [MPSTATS Ozon API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-product-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [LinkFox Tool Gateway Product Search Endpoint](https://tool-gateway.linkfox.com/mpstats/ozon/productSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries or tables of product identity fields; direct script execution can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY. Requests must include at least one keyword, SKU, brand, or seller filter.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
