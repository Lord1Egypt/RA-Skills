## Description: <br>
Analyzes an existing product list and groups items by visual similarity of their main images for lookalike detection, deduplication, and visual clustering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and product operators use this skill after product search or recommendation steps to cluster visually similar product images, find near-duplicates, and identify cross-brand lookalikes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product data, image URLs, business metrics, and user query text to LinkFox for analysis. <br>
Mitigation: Use it only when users trust LinkFox with that product and business context, and avoid sending sensitive or unnecessary data. <br>
Risk: The documented feedback workflow can send feedback or conversation context to a separate LinkFox feedback endpoint without clear user consent. <br>
Mitigation: Disable or avoid automatic feedback reporting unless the user explicitly approves sharing feedback and related context. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-multimodal-product-similarity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON API responses with markdown summaries and product-grouping tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing products array, image URLs, and a LINKFOXAGENT_API_KEY; outputs similarity groups, analysis metadata, and tabular product details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
